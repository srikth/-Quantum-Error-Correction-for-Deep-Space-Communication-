 import numpy as np
import torch
from qec.steane import logical_zero
from qec.error_models import deep_space_noise, apply_pauli

def extract_features(state):
    return np.concatenate([np.real(state), np.imag(state)])

def fidelity(a, b):
    return abs(np.vdot(a, b))**2

def decode_prediction(pred):
    pred_class = torch.argmax(pred).item()
    qubit = pred_class // 4
    error_type_idx = pred_class % 4
    error_map = {0:'I',1:'X',2:'Y',3:'Z'}
    return qubit, error_map[error_type_idx]

def apply_correction(state, qubit, error_type):
    if error_type == 'I':
        return state
    return apply_pauli(state, qubit, error_type)

def run_trial(model, distance):
    original = logical_zero()
    noisy = deep_space_noise(original.copy(), distance)

    f_before = fidelity(original, noisy)

    features = extract_features(noisy)
    pred = model(torch.tensor(features, dtype=torch.float32))

    q, e = decode_prediction(pred)
    corrected = apply_correction(noisy, q, e)

    f_after = fidelity(original, corre
 import numpy as np
import torch
from qec.steane import logical_zero
from qec.error_models import deep_space_noise, apply_pauli

def extract_features(state):
    return np.concatenate([np.real(state), np.imag(state)])

def fidelity(a, b):
    return abs(np.vdot(a, b))**2

def decode_prediction(pred):
    pred_class = torch.argmax(pred).item()
    qubit = pred_class // 4
    error_type_idx = pred_class % 4
    error_map = {0:'I',1:'X',2:'Y',3:'Z'}
    return qubit, error_map[error_type_idx]

def apply_correction(state, qubit, error_type):
    if error_type == 'I':
        return state
    return apply_pauli(state, qubit, error_type)

def run_trial(model, distance):
    original = logical_zero()
    noisy = deep_space_noise(original.copy(), distance)
   f_before = fidelity(original, noisy)

    features = extract_features(noisy)
    pred = model(torch.tensor(features, dtype=torch.float32))

    q, e = decode_prediction(pred)
    corrected = apply_correction(noisy, q, e)

    f_after = fidelity(original, corrected)

    return f_before, f_after
