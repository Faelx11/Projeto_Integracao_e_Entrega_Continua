import math
from collections import Counter

class Recognizer:
    def __init__(self, user_store, purchase_store, threshold=0.75):
        self.user_store = user_store
        self.purchase_store = purchase_store
        self.threshold = threshold

    def _profile_signature(self, purchases):
        # signature: counts of items and colors + average price
        items = Counter([p['item'] for p in purchases])
        colors = Counter([p['color'] for p in purchases])
        avg_price = sum([p['price'] for p in purchases]) / len(purchases) if purchases else 0.0
        sig = {}
        # keep top keys deterministic
        for k, v in items.items():
            sig[f'item:{k}'] = v
        for k, v in colors.items():
            sig[f'color:{k}'] = v
        sig['price_avg'] = avg_price
        return sig

    def _vectorize(self, sig, keys):
        return [sig.get(k, 0.0) for k in keys]

    def _cosine_similarity(self, a, b):
        dot = sum(x*y for x,y in zip(a,b))
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(x*x for x in b))
        if na==0 or nb==0:
            return 0.0
        return dot/(na*nb)

    def _aggregate_signatures(self):
        # build combined key set
        user_sigs = {}
        keys = set()
        for uid in self.user_store.all_ids():
            purchases = self.purchase_store.purchases_by_user(uid)
            sig = self._profile_signature(purchases)
            user_sigs[uid] = sig
            keys.update(sig.keys())
        keys = sorted(list(keys))
        # vectorize
        vecs = {uid: self._vectorize(sig, keys) for uid, sig in user_sigs.items()}
        return keys, vecs

    def recognize_by_purchase(self, purchase):
        # create temporary signature for single purchase
        sig = {}
        sig[f"item:{purchase['item'].lower()}"] = 1
        sig[f"color:{purchase['color'].lower()}"] = 1
        sig['price_avg'] = float(purchase['price'])
        keys, vecs = self._aggregate_signatures()
        if not vecs:
            return None
        # ensure keys include new sig keys
        for k in sig.keys():
            if k not in keys:
                keys.append(k)
        target = self._vectorize(sig, keys)
        best_uid = None
        best_score = 0.0
        for uid, vec in vecs.items():
            # extend vec if needed
            if len(vec) < len(keys):
                vec = vec + [0.0]*(len(keys)-len(vec))
            score = self._cosine_similarity(target, vec)
            if score > best_score:
                best_score = score
                best_uid = uid
        if best_score >= self.threshold:
            return best_uid
        return None

    def public_view(self):
        # group users by style signature (simple: by hashing signature keys)
        keys, vecs = self._aggregate_signatures()
        style_map = {}
        style_list = []
        # naive clustering: identical signature keys => same style
        for uid, vec in vecs.items():
            key = tuple(vec)
            if key not in style_map:
                style_map[key] = len(style_map) + 1
            style_id = style_map[key]
            style_list.append((uid, style_id))
        # produce public purchases with anonymized style identifier
        public = []
        purchases = self.purchase_store.all()
        for p in purchases:
            # find style id
            sid = None
            for uid, st in style_list:
                if uid == p['user_id']:
                    sid = st
                    break
            label = f'Cliente Estilo #{sid}' if sid is not None else 'Cliente Estilo #?'
            public.append(f"{label} - {p['item']} ({p['color']}) - R$ {p['price']:.2f} - {p['date']}")
        return public
