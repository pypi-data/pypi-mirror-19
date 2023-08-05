# encoding: utf8
from __future__ import unicode_literals

from ..symbols import *


TAG_MAP = {
    "$(":       {POS: PUNCT, "PunctType": "brck"},
    "$,":       {POS: PUNCT, "PunctType": "comm"},
    "$.":       {POS: PUNCT, "PunctType": "peri"},
    "ADJA":     {POS: ADJ},
    "ADJD":     {POS: ADJ, "Variant": "short"},
    "ADV":      {POS: ADV},
    "APPO":     {POS: ADP, "AdpType": "post"},
    "APPR":     {POS: ADP, "AdpType": "prep"},
    "APPRART":  {POS: ADP, "AdpType": "prep", "PronType": "art"},
    "APZR":     {POS: ADP, "AdpType": "circ"},
    "ART":      {POS: DET, "PronType": "art"},
    "CARD":     {POS: NUM, "NumType": "card"},
    "FM":       {POS: X, "Foreign": "yes"},
    "ITJ":      {POS: INTJ},
    "KOKOM":    {POS: CONJ, "ConjType": "comp"},
    "KON":      {POS: CONJ},
    "KOUI":     {POS: SCONJ},
    "KOUS":     {POS: SCONJ},
    "NE":       {POS: PROPN},
    "NNE":      {POS: PROPN},
    "NN":       {POS: NOUN},
    "PAV":      {POS: ADV, "PronType": "dem"},
    "PROAV":    {POS: ADV, "PronType": "dem"},
    "PDAT":     {POS: DET, "PronType": "dem"},
    "PDS":      {POS: PRON, "PronType": "dem"},
    "PIAT":     {POS: DET, "PronType": "ind|neg|tot"},
    "PIDAT":    {POS: DET, "AdjType": "pdt", "PronType": "ind|neg|tot"},
    "PIS":      {POS: PRON, "PronType": "ind|neg|tot"},
    "PPER":     {POS: PRON, "PronType": "prs"},
    "PPOSAT":   {POS: DET, "Poss": "yes", "PronType": "prs"},
    "PPOSS":    {POS: PRON, "Poss": "yes", "PronType": "prs"},
    "PRELAT":   {POS: DET, "PronType": "rel"},
    "PRELS":    {POS: PRON, "PronType": "rel"},
    "PRF":      {POS: PRON, "PronType": "prs", "Reflex": "yes"},
    "PTKA":     {POS: PART},
    "PTKANT":   {POS: PART, "PartType": "res"},
    "PTKNEG":   {POS: PART, "Negative": "yes"},
    "PTKVZ":    {POS: PART, "PartType": "vbp"},
    "PTKZU":    {POS: PART, "PartType": "inf"},
    "PWAT":     {POS: DET, "PronType": "int"},
    "PWAV":     {POS: ADV, "PronType": "int"},
    "PWS":      {POS: PRON, "PronType": "int"},
    "TRUNC":    {POS: X, "Hyph": "yes"},
    "VAFIN":    {POS: AUX, "Mood": "ind", "VerbForm": "fin"},
    "VAIMP":    {POS: AUX, "Mood": "imp", "VerbForm": "fin"},
    "VAINF":    {POS: AUX, "VerbForm": "inf"},
    "VAPP":     {POS: AUX, "Aspect": "perf", "VerbForm": "part"},
    "VMFIN":    {POS: VERB, "Mood": "ind", "VerbForm": "fin", "VerbType": "mod"},
    "VMINF":    {POS: VERB, "VerbForm": "inf", "VerbType": "mod"},
    "VMPP":     {POS: VERB, "Aspect": "perf", "VerbForm": "part", "VerbType": "mod"},
    "VVFIN":    {POS: VERB, "Mood": "ind", "VerbForm": "fin"},
    "VVIMP":    {POS: VERB, "Mood": "imp", "VerbForm": "fin"},
    "VVINF":    {POS: VERB, "VerbForm": "inf"},
    "VVIZU":    {POS: VERB, "VerbForm": "inf"},
    "VVPP":     {POS: VERB, "Aspect": "perf", "VerbForm": "part"},
    "XY":       {POS: X},
    "SP":       {POS: SPACE}
}
