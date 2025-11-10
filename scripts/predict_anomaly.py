#!/usr/bin/env python3
"""Load saved autoencoder and scaler, compute reconstruction error and flag anomalies.

This script is resilient: if numpy/torch are not available it falls back to a simple heuristic
score so the pipeline can continue in minimal development environments.

Usage:
  python3 scripts/predict_anomaly.py --model models/autoencoder.pt --scaler models/scaler.joblib --in data/sample.jsonl --out predictions.jsonl
"""
import argparse
import json
from pathlib import Path

# loader fallbacks
try:
    import joblib
except Exception:
    joblib = None
    import pickle

# optional heavy deps
try:
    import numpy as np
except Exception:
    np = None
try:
    import torch
    import torch.nn as nn
except Exception:
    torch = None
    nn = None


class _Dummy:
    pass


class Autoencoder(nn.Module if nn is not None else _Dummy):
    def __init__(self, n_features, hidden=8):
        if nn is None:
            return
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(n_features, hidden),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden, n_features),
        )

    def forward(self, x):
        if nn is None:
            return x
        z = self.encoder(x)
        return self.decoder(z)


def load_model_state(path, n_features):
    # If torch not available or model placeholder, return None
    if torch is None:
        return None
    try:
        model = Autoencoder(n_features)
        model.load_state_dict(torch.load(path, map_location='cpu'))
        model.eval()
        return model
    except Exception:
        # model file may be placeholder text
        return None


def extract_features_from_record(rec):
    hour = rec.get('hour') if rec.get('hour') is not None else -1
    dow = rec.get('dow') if rec.get('dow') is not None else -1
    is_saas = 1 if rec.get('is_saas') else 0
    return [float(hour), float(dow), float(is_saas)]


def simple_heuristic_score(feats):
    # feats: [hour, dow, is_saas]
    hour, dow, is_saas = feats
    score = 0.0
    # SaaS traffic is slightly more suspicious by default
    score += 0.5 * float(is_saas)
    try:
        # outside business hours (9-17) increases score
        if hour < 9 or hour > 17:
            score += 0.25
    except Exception:
        pass
    try:
        # weekend (sat=5,sun=6) increases score a bit
        if int(dow) in (5, 6):
            score += 0.25
    except Exception:
        pass
    # clamp to [0,1]
    return min(1.0, max(0.0, score))


def load_threshold(path):
    if not path:
        return None
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh).get('threshold')
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--scaler', required=True)
    p.add_argument('--in', dest='infile', required=True)
    p.add_argument('--out', default='predictions.jsonl')
    p.add_argument('--threshold', help='optional threshold json to override')
    args = p.parse_args()

    # load scaler (joblib or pickle)
    scaler = None
    try:
        if joblib:
            scaler = joblib.load(args.scaler)
        else:
            with open(args.scaler, 'rb') as fh:
                scaler = pickle.load(fh)
    except Exception:
        scaler = None

    # set up model if possible
    n_features = 3
    model = load_model_state(args.model, n_features)

    threshold = load_threshold(args.threshold) if args.threshold else None

    # if no threshold provided, try to load from models/threshold.json next to scaler
    if threshold is None:
        thr_path = Path(args.scaler).with_name('threshold.json')
        if thr_path.exists():
            try:
                with open(thr_path, encoding='utf-8') as fh:
                    threshold = json.load(fh).get('threshold')
            except Exception:
                threshold = None

    # default threshold if nothing found
    if threshold is None:
        threshold = 0.5

    outp = Path(args.out)
    with open(args.infile, encoding='utf-8') as inh, outp.open('w', encoding='utf-8') as outh:
        for line in inh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            feats = extract_features_from_record(rec)

            # If we have numpy + torch + model + scaler, do real prediction
            if (np is not None) and (torch is not None) and (model is not None) and (scaler is not None):
                try:
                    Xs = scaler.transform([feats])
                    arr = torch.from_numpy(Xs).float()
                    with torch.no_grad():
                        recon = model(arr).numpy()
                    err = float(((recon - Xs) ** 2).mean())
                    is_anom = err > threshold
                except Exception:
                    # fallback to heuristic on any runtime error
                    err = simple_heuristic_score(feats)
                    is_anom = err > threshold
            else:
                # not enough libs / model missing — use heuristic
                err = simple_heuristic_score(feats)
                is_anom = err > threshold

            outh.write(json.dumps({'record': rec, 'anomaly_score': err, 'anomaly': bool(is_anom)}) + '\n')

    print('Wrote predictions to', outp)


if __name__ == '__main__':
    main()
