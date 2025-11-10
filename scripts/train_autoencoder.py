#!/usr/bin/env python3
"""Train a small autoencoder on cleaned dataset JSONL and save model + scaler + threshold.

Input: cleaned JSONL produced by prepare_dataset.py (fields: ts, hour, dow, is_saas, src_ip...)
Output: models/autoencoder.pt, models/scaler.joblib, models/threshold.json

Usage:
  python3 scripts/train_autoencoder.py --in data/cleaned.jsonl --out models --epochs 20
"""
import argparse
import json
import os
from pathlib import Path

try:
    import joblib
except Exception:
    joblib = None
    import pickle

try:
    import numpy as np
    import torch
    import torch.nn as nn
except Exception:
    np = None
    torch = None
    nn = None
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler


class Autoencoder(nn.Module):
    def __init__(self, n_features, hidden=8):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(n_features, hidden),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden, n_features),
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)


def load_data(path):
    X = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            # features: hour, dow, is_saas
            hour = rec.get('hour') if rec.get('hour') is not None else -1
            dow = rec.get('dow') if rec.get('dow') is not None else -1
            is_saas = 1 if rec.get('is_saas') else 0
            X.append([float(hour), float(dow), float(is_saas)])
    return np.array(X, dtype=float)


def train(X, epochs=20, lr=1e-3):
    device = torch.device('cpu')
    n_features = X.shape[1]
    model = Autoencoder(n_features)
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    data = torch.from_numpy(X).float()

    for ep in range(epochs):
        model.train()
        opt.zero_grad()
        out = model(data)
        loss = loss_fn(out, data)
        loss.backward()
        opt.step()
        if (ep + 1) % 5 == 0 or ep == 0:
            print(f'epoch {ep+1}/{epochs} loss={loss.item():.6f}')

    # compute reconstruction errors
    model.eval()
    with torch.no_grad():
        recon = model(data).numpy()
    errors = np.mean((recon - X) ** 2, axis=1)
    return model, errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--in', '-i', dest='infile', required=True)
    p.add_argument('--out', '-o', default='models')
    p.add_argument('--epochs', type=int, default=20)
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    X = load_data(args.infile)
    if not X or (np is None):
        # Missing numpy/torch or no data: create placeholder scaler + threshold
        print('numpy/torch not available or no data - creating placeholder artifacts')
        scaler_obj = StandardScaler()
        # fit on a tiny sample to avoid empty scaler
        scaler_obj.fit([[0.0, 0.0, 0.0]])
        if joblib:
            joblib.dump(scaler_obj, Path(args.out) / 'scaler.joblib')
        else:
            with open(Path(args.out) / 'scaler.joblib', 'wb') as fh:
                pickle.dump(scaler_obj, fh)
        with open(Path(args.out) / 'threshold.json', 'w', encoding='utf-8') as fh:
            json.dump({'mean': 0.0, 'std': 0.0, 'threshold': 0.5}, fh)
        # create empty model file as placeholder
        Path(args.out).mkdir(parents=True, exist_ok=True)
        Path(args.out, 'autoencoder.pt').write_text('placeholder')
        print('Wrote placeholder model and artifacts')
        return

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    model, errors = train(Xs, epochs=args.epochs)

    # threshold: mean + 3*std
    mean = float(errors.mean())
    std = float(errors.std())
    threshold = mean + 3 * std

    # save model and scaler
    model_path = Path(args.out) / 'autoencoder.pt'
    torch.save(model.state_dict(), str(model_path))
    if joblib:
        joblib.dump(scaler, Path(args.out) / 'scaler.joblib')
    else:
        # fallback to pickle
        with open(Path(args.out) / 'scaler.joblib', 'wb') as fh:
            pickle.dump(scaler, fh)
    with open(Path(args.out) / 'threshold.json', 'w', encoding='utf-8') as fh:
        json.dump({'mean': mean, 'std': std, 'threshold': threshold}, fh)

    print('Saved model to', model_path)
    print('Threshold:', threshold)


if __name__ == '__main__':
    main()
