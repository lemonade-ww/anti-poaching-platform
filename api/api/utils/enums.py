from enum import Enum, auto


class ConservationStatus(Enum):
    EX = auto()  # Extinct
    EW = auto()  # Extinct in the wild
    CR = auto()  # Critically endangered
    EN = auto()  # Endangered
    VU = auto()  # Vulnerable
    NT = auto()  # Near threatened
    CD = auto()  # Conservation Dependent
    LC = auto()  # Least concern
    DD = auto()  # Data deficient
    NE = auto()  # Not evaluated


class ProtectionClass(Enum):
    I = 0
    II = 1
