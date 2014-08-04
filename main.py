from itertools import product
from random import randint
import random
from collections import Counter
from collections import defaultdict


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return '%s_%s' % (self.face, self.suit[0])

FACES = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
SUITS = ['spade', 'heart', 'club', 'diamond']

DECK = [Card(*card_info) for card_info in product(SUITS, FACES)]
HAND = []

CARD_INDEX_BEGIN = 0
CARD_INDEX_END = 51
CARD_INDEX_HALF = 26
CARD_HANDFUL_COUNT = 7


def shuffle_overhand():
    global DECK
    cut = randint(CARD_INDEX_BEGIN + 1, CARD_INDEX_END - 1)
    DECK = DECK[cut:] + DECK[:cut]


def shuffle_riffle():
    global DECK
    DECK = [x for tup in zip(DECK[:CARD_INDEX_HALF], DECK[CARD_INDEX_HALF:]) for x in tup]


# def shuffle():
#     for i in range(0, randint(10, 20)):
#         if randint(0, 1):
#             shuffle_overhand()
#         else:
#             shuffle_riffle()
def shuffle():
    random.shuffle(DECK)


def deal():
    global HAND, DECK
    HAND = DECK[:CARD_HANDFUL_COUNT]


statistics = defaultdict(int)
statistics_total_hands = 0
evaluate_result = defaultdict(bool)


def evaluate(five_cards):
    assert(len(five_cards) == 5)

    faces = [c.face for c in five_cards]
    suits = [c.suit for c in five_cards]

    face_count = list(Counter(faces).values())
    suit_count = list(Counter(suits).values())

    def royal_straight():
        return flush_raw() and straight_raw()

    def four_of_a_kind():
        return 4 in face_count

    def full_house():
        return (3 in face_count) and (2 in face_count)

    def flush_raw():
        return 5 in suit_count

    def flush():
        return flush_raw() and not straight_raw()

    def straight_raw():
        def face_to_int(face):
            try:
                return int(face)
            except ValueError:
                return {
                    'J': 11,
                    'Q': 12,
                    'K': 13,
                    'A': 14
                }[face]
        int_faces = [face_to_int(face) for face in faces]
        int_faces.sort()
        return max(face_count) == 1 and \
            (int_faces[-1] - int_faces[0] == 4 or int_faces == [2, 3, 4, 5, 14])

    def straight():
        return straight_raw() and not flush_raw()

    def three_of_a_kind():
        return (3 in face_count) and (2 not in face_count)

    def two_pairs():
        return face_count.count(2) == 2

    def one_pair():
        return face_count.count(2) == 1 and face_count.count(1) == 3

    judge_list = [
        one_pair,
        two_pairs,
        three_of_a_kind,
        straight,
        flush,
        full_house,
        four_of_a_kind,
        royal_straight
    ]

    for func in judge_list:
        if func():
            return func.__name__

    return 'nothing'


def show_deck():
    print(DECK)


def show_hand():
    print(HAND)


def choose_5_from_7(list_of_seven):
    assert(len(list_of_seven) == 7)

    for i in range(0, 7):
        for j in range(i + 1, 7):
            l = list_of_seven[:]
            l.pop(j)
            l.pop(i)
            yield l


def show_statistics():
    print('statistics:')
    for key in sorted(statistics.keys()):
        print(key, statistics[key], statistics[key] / statistics_total_hands * 100)
    print('total:', statistics_total_hands)


def evaluate_hand():
    for combination in choose_5_from_7(HAND):
        evaluate_result[evaluate(combination)] = True


def add_to_statistics():
    global statistics_total_hands
    try:
        del evaluate_result['nothing']
    except KeyError:
        pass
    for key in evaluate_result:
        if evaluate_result[key]:
            statistics[key] += 1
    if len(evaluate_result.keys()) == 0:
        statistics['nothing'] += 1
    statistics_total_hands += 1


def main():
    for i in range(0, 100000000):
        shuffle()
        deal()
        evaluate_hand()
        add_to_statistics()
        evaluate_result.clear()
        if i % 10000 == 0:
            print(i)
    show_statistics()

main()