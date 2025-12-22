"""
Tests for Task 4: Playing Card Magic Trick with Quantum States

These tests validate the quantum card representation, tensor products,
inner products, probabilities, and superposition states.
"""

import pytest
import numpy as np


class TestRankBasisStates:
    """Test rank basis state creation and properties."""

    @pytest.fixture
    def ranks(self):
        """Create all 8 rank basis states."""
        rank_7 = np.array([[1], [0], [0], [0], [0], [0], [0], [0]])
        rank_8 = np.array([[0], [1], [0], [0], [0], [0], [0], [0]])
        rank_9 = np.array([[0], [0], [1], [0], [0], [0], [0], [0]])
        rank_10 = np.array([[0], [0], [0], [1], [0], [0], [0], [0]])
        rank_J = np.array([[0], [0], [0], [0], [1], [0], [0], [0]])
        rank_Q = np.array([[0], [0], [0], [0], [0], [1], [0], [0]])
        rank_K = np.array([[0], [0], [0], [0], [0], [0], [1], [0]])
        rank_A = np.array([[0], [0], [0], [0], [0], [0], [0], [1]])
        return [rank_7, rank_8, rank_9, rank_10, rank_J, rank_Q, rank_K, rank_A]

    def test_rank_dimensions(self, ranks):
        """Test that all ranks have correct dimensions."""
        for rank in ranks:
            assert rank.shape == (8, 1), "Rank should be 8×1 column vector"

    def test_rank_normalization(self, ranks):
        """Test that all ranks are normalized."""
        for rank in ranks:
            norm = np.linalg.norm(rank)
            assert np.isclose(norm, 1.0), f"Rank should have norm 1, got {norm}"

    def test_rank_orthogonality(self, ranks):
        """Test that different ranks are orthogonal."""
        for i, rank_i in enumerate(ranks):
            for j, rank_j in enumerate(ranks):
                inner = np.dot(rank_i.T, rank_j)[0, 0]
                if i == j:
                    assert np.isclose(inner, 1.0), "Same rank should have inner product 1"
                else:
                    assert np.abs(inner) < 1e-10, "Different ranks should be orthogonal"

    def test_rank_basis_completeness(self, ranks):
        """Test that ranks form a complete basis."""
        # Create identity matrix from outer products
        identity = sum(np.dot(rank, rank.T) for rank in ranks)
        expected_identity = np.eye(8)

        assert np.allclose(identity, expected_identity), \
            "Ranks should form complete orthonormal basis"


class TestSuitBasisStates:
    """Test suit basis state creation and properties."""

    @pytest.fixture
    def suits(self):
        """Create all 4 suit basis states."""
        spades = np.array([[1], [0], [0], [0]])
        hearts = np.array([[0], [1], [0], [0]])
        diamonds = np.array([[0], [0], [1], [0]])
        clubs = np.array([[0], [0], [0], [1]])
        return [spades, hearts, diamonds, clubs]

    def test_suit_dimensions(self, suits):
        """Test that all suits have correct dimensions."""
        for suit in suits:
            assert suit.shape == (4, 1), "Suit should be 4×1 column vector"

    def test_suit_normalization(self, suits):
        """Test that all suits are normalized."""
        for suit in suits:
            norm = np.linalg.norm(suit)
            assert np.isclose(norm, 1.0), f"Suit should have norm 1, got {norm}"

    def test_suit_orthogonality(self, suits):
        """Test that different suits are orthogonal."""
        for i, suit_i in enumerate(suits):
            for j, suit_j in enumerate(suits):
                inner = np.dot(suit_i.T, suit_j)[0, 0]
                if i == j:
                    assert np.isclose(inner, 1.0), "Same suit should have inner product 1"
                else:
                    assert np.abs(inner) < 1e-10, "Different suits should be orthogonal"

    def test_suit_basis_completeness(self, suits):
        """Test that suits form a complete basis."""
        identity = sum(np.dot(suit, suit.T) for suit in suits)
        expected_identity = np.eye(4)

        assert np.allclose(identity, expected_identity), \
            "Suits should form complete orthonormal basis"


class TestKroneckerProducts:
    """Test Kronecker product operations."""

    def test_kron_dimensions(self):
        """Test that Kronecker product has correct dimensions."""
        a = np.array([[1], [0]])
        b = np.array([[1], [0], [0]])

        result = np.kron(a, b)

        assert result.shape == (6, 1), "Kronecker product should be 6×1"

    def test_kron_simple_example(self):
        """Test Kronecker product with simple example."""
        a = np.array([[1], [0]])
        b = np.array([[0], [1]])

        result = np.kron(a, b)
        expected = np.array([[0], [1], [0], [0]])

        assert np.allclose(result, expected), \
            "Kronecker product should match expected result"

    def test_kron_preserves_normalization(self):
        """Test that Kronecker product preserves normalization."""
        a = np.array([[1], [0]])  # Normalized
        b = np.array([[1], [0], [0], [0]])  # Normalized

        result = np.kron(a, b)
        norm = np.linalg.norm(result)

        assert np.isclose(norm, 1.0), \
            "Kronecker product of normalized vectors should be normalized"


class TestCardStates:
    """Test card state construction."""

    @pytest.fixture
    def ranks(self):
        """Create rank basis states."""
        return [
            np.array([[1], [0], [0], [0], [0], [0], [0], [0]]),  # 7
            np.array([[0], [1], [0], [0], [0], [0], [0], [0]]),  # 8
            np.array([[0], [0], [1], [0], [0], [0], [0], [0]]),  # 9
            np.array([[0], [0], [0], [1], [0], [0], [0], [0]]),  # 10
            np.array([[0], [0], [0], [0], [1], [0], [0], [0]]),  # J
            np.array([[0], [0], [0], [0], [0], [1], [0], [0]]),  # Q
            np.array([[0], [0], [0], [0], [0], [0], [1], [0]]),  # K
            np.array([[0], [0], [0], [0], [0], [0], [0], [1]]),  # A
        ]

    @pytest.fixture
    def suits(self):
        """Create suit basis states."""
        return [
            np.array([[1], [0], [0], [0]]),  # Spades
            np.array([[0], [1], [0], [0]]),  # Hearts
            np.array([[0], [0], [1], [0]]),  # Diamonds
            np.array([[0], [0], [0], [1]]),  # Clubs
        ]

    def test_card_dimensions(self, ranks, suits):
        """Test that card states have correct dimensions."""
        card = np.kron(ranks[0], suits[0])
        assert card.shape == (32, 1), "Card should be 32×1 vector"

    def test_card_normalization(self, ranks, suits):
        """Test that card states are normalized."""
        for rank in ranks:
            for suit in suits:
                card = np.kron(rank, suit)
                norm = np.linalg.norm(card)
                assert np.isclose(norm, 1.0), \
                    f"Card should have norm 1, got {norm}"

    def test_different_cards_orthogonal(self, ranks, suits):
        """Test that different cards are orthogonal."""
        card1 = np.kron(ranks[0], suits[0])  # 7 of Spades
        card2 = np.kron(ranks[1], suits[0])  # 8 of Spades
        card3 = np.kron(ranks[0], suits[1])  # 7 of Hearts

        inner12 = np.dot(card1.T, card2)[0, 0]
        inner13 = np.dot(card1.T, card3)[0, 0]

        assert np.abs(inner12) < 1e-10, "Different ranks should be orthogonal"
        assert np.abs(inner13) < 1e-10, "Different suits should be orthogonal"

    def test_same_card_inner_product(self, ranks, suits):
        """Test that same card has inner product 1."""
        card = np.kron(ranks[0], suits[0])
        inner = np.dot(card.T, card)[0, 0]

        assert np.isclose(inner, 1.0), \
            "Same card should have inner product 1"

    def test_all_32_cards_orthonormal(self, ranks, suits):
        """Test that all 32 cards are orthonormal."""
        cards = []
        for rank in ranks:
            for suit in suits:
                cards.append(np.kron(rank, suit))

        # Check orthonormality
        for i, card_i in enumerate(cards):
            for j, card_j in enumerate(cards):
                inner = np.dot(card_i.T, card_j)[0, 0]
                if i == j:
                    assert np.isclose(inner, 1.0), \
                        f"Card {i} should have norm 1"
                else:
                    assert np.abs(inner) < 1e-10, \
                        f"Cards {i} and {j} should be orthogonal"


class TestInnerProducts:
    """Test inner product calculations."""

    def test_inner_product_same_vector(self):
        """Test inner product of vector with itself."""
        v = np.array([[1], [0], [0]])
        inner = np.dot(v.T.conj(), v)[0, 0]

        assert np.isclose(inner, 1.0), "⟨v|v⟩ should be 1"

    def test_inner_product_orthogonal_vectors(self):
        """Test inner product of orthogonal vectors."""
        v1 = np.array([[1], [0], [0]])
        v2 = np.array([[0], [1], [0]])

        inner = np.dot(v1.T.conj(), v2)[0, 0]

        assert np.abs(inner) < 1e-10, "Orthogonal vectors should have inner product 0"

    def test_inner_product_complex_vectors(self):
        """Test inner product with complex vectors."""
        v1 = np.array([[1], [1j]]) / np.sqrt(2)
        v2 = np.array([[1], [-1j]]) / np.sqrt(2)

        inner = np.dot(v1.T.conj(), v2)[0, 0]

        # These are orthogonal
        assert np.abs(inner) < 1e-10, "Complex orthogonal vectors"


class TestProbabilities:
    """Test probability calculations."""

    def test_probability_calculation(self):
        """Test basic probability calculation."""
        state1 = np.array([[1], [0]])
        state2 = np.array([[1], [0]])

        inner = np.dot(state1.T.conj(), state2)[0, 0]
        prob = np.abs(inner)**2

        assert np.isclose(prob, 1.0), "Identical states should have probability 1"

    def test_probability_orthogonal_states(self):
        """Test probability for orthogonal states."""
        state1 = np.array([[1], [0]])
        state2 = np.array([[0], [1]])

        inner = np.dot(state1.T.conj(), state2)[0, 0]
        prob = np.abs(inner)**2

        assert prob < 1e-10, "Orthogonal states should have probability 0"

    def test_probabilities_sum_to_one(self):
        """Test that probabilities over complete basis sum to 1."""
        # System state
        state = np.array([[1], [0], [0], [0]])

        # Basis states
        basis = [
            np.array([[1], [0], [0], [0]]),
            np.array([[0], [1], [0], [0]]),
            np.array([[0], [0], [1], [0]]),
            np.array([[0], [0], [0], [1]]),
        ]

        # Calculate probabilities
        total_prob = sum(np.abs(np.dot(b.T.conj(), state)[0, 0])**2 for b in basis)

        assert np.isclose(total_prob, 1.0), "Probabilities should sum to 1"


class TestSuperposition:
    """Test superposition state creation and properties."""

    def test_equal_superposition_two_states(self):
        """Test equal superposition of two basis states."""
        state1 = np.array([[1], [0]])
        state2 = np.array([[0], [1]])

        superposition = (state1 + state2) / np.sqrt(2)

        # Check normalization
        norm = np.linalg.norm(superposition)
        assert np.isclose(norm, 1.0), "Superposition should be normalized"

        # Check probabilities
        prob1 = np.abs(np.dot(state1.T.conj(), superposition)[0, 0])**2
        prob2 = np.abs(np.dot(state2.T.conj(), superposition)[0, 0])**2

        assert np.isclose(prob1, 0.5), "Probability should be 0.5"
        assert np.isclose(prob2, 0.5), "Probability should be 0.5"

    def test_unequal_superposition(self):
        """Test unequal superposition."""
        state1 = np.array([[1], [0]])
        state2 = np.array([[0], [1]])

        alpha = np.sqrt(0.7)
        beta = np.sqrt(0.3)
        superposition = alpha * state1 + beta * state2

        # Check normalization
        norm = np.linalg.norm(superposition)
        assert np.isclose(norm, 1.0), "Superposition should be normalized"

        # Check probabilities
        prob1 = np.abs(np.dot(state1.T.conj(), superposition)[0, 0])**2
        prob2 = np.abs(np.dot(state2.T.conj(), superposition)[0, 0])**2

        assert np.isclose(prob1, 0.7, atol=1e-10), "Probability should be 0.7"
        assert np.isclose(prob2, 0.3, atol=1e-10), "Probability should be 0.3"

    def test_superposition_four_states(self):
        """Test equal superposition of four states."""
        states = [
            np.array([[1], [0], [0], [0]]),
            np.array([[0], [1], [0], [0]]),
            np.array([[0], [0], [1], [0]]),
            np.array([[0], [0], [0], [1]]),
        ]

        superposition = sum(states) / 2.0  # 1/sqrt(4) = 1/2

        # Check normalization
        norm = np.linalg.norm(superposition)
        assert np.isclose(norm, 1.0), "Superposition should be normalized"

        # Check equal probabilities
        for state in states:
            prob = np.abs(np.dot(state.T.conj(), superposition)[0, 0])**2
            assert np.isclose(prob, 0.25), "Each state should have probability 0.25"


class TestMagicTrick:
    """Test the magic trick implementation."""

    @pytest.fixture
    def all_cards(self):
        """Create all 32 card states."""
        ranks = [
            np.array([[1], [0], [0], [0], [0], [0], [0], [0]]),
            np.array([[0], [1], [0], [0], [0], [0], [0], [0]]),
            np.array([[0], [0], [1], [0], [0], [0], [0], [0]]),
            np.array([[0], [0], [0], [1], [0], [0], [0], [0]]),
            np.array([[0], [0], [0], [0], [1], [0], [0], [0]]),
            np.array([[0], [0], [0], [0], [0], [1], [0], [0]]),
            np.array([[0], [0], [0], [0], [0], [0], [1], [0]]),
            np.array([[0], [0], [0], [0], [0], [0], [0], [1]]),
        ]
        suits = [
            np.array([[1], [0], [0], [0]]),
            np.array([[0], [1], [0], [0]]),
            np.array([[0], [0], [1], [0]]),
            np.array([[0], [0], [0], [1]]),
        ]

        cards = {}
        rank_names = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suit_names = ['S', 'H', 'D', 'C']

        for rank_name, rank in zip(rank_names, ranks):
            for suit_name, suit in zip(suit_names, suits):
                card_name = f"{rank_name}{suit_name}"
                cards[card_name] = np.kron(rank, suit)

        return cards

    def test_target_in_superposition(self, all_cards):
        """Test magic trick when target is in superposition."""
        # Superposition of all Aces
        superposition = (
            all_cards['AS'] + all_cards['AH'] +
            all_cards['AD'] + all_cards['AC']
        ) / 2.0

        # Target: Ace of Hearts
        target = all_cards['AH']

        # Calculate probability
        inner = np.dot(target.T.conj(), superposition)[0, 0]
        prob = np.abs(inner)**2

        assert np.isclose(prob, 0.25), \
            "Probability should be 1/4 for 4-card superposition"

    def test_target_not_in_superposition(self, all_cards):
        """Test magic trick when target is NOT in superposition."""
        # Superposition of all Aces
        superposition = (
            all_cards['AS'] + all_cards['AH'] +
            all_cards['AD'] + all_cards['AC']
        ) / 2.0

        # Target: 7 of Spades (not an Ace)
        target = all_cards['7S']

        # Calculate probability
        inner = np.dot(target.T.conj(), superposition)[0, 0]
        prob = np.abs(inner)**2

        assert prob < 1e-10, \
            "Probability should be 0 when target not in superposition"

    def test_probabilities_sum_correctly(self, all_cards):
        """Test that probabilities sum to 1 for a superposition."""
        # Superposition of 4 specific cards
        cards_in_super = ['7S', '9H', 'QD', 'KC']
        superposition = sum(all_cards[c] for c in cards_in_super) / 2.0

        # Calculate probabilities for all cards
        total_prob = 0
        for card_state in all_cards.values():
            inner = np.dot(card_state.T.conj(), superposition)[0, 0]
            prob = np.abs(inner)**2
            total_prob += prob

        assert np.isclose(total_prob, 1.0), \
            "Total probability over all cards should be 1"


class TestIntegration:
    """Integration tests combining multiple concepts."""

    def test_complete_card_system(self):
        """Test complete card system with all operations."""
        # Create ranks and suits
        ranks = [np.zeros((8, 1)) for _ in range(8)]
        for i in range(8):
            ranks[i][i, 0] = 1

        suits = [np.zeros((4, 1)) for _ in range(4)]
        for i in range(4):
            suits[i][i, 0] = 1

        # Create all cards
        cards = []
        for rank in ranks:
            for suit in suits:
                card = np.kron(rank, suit)
                cards.append(card)

        # Verify we have 32 cards
        assert len(cards) == 32, "Should have 32 cards"

        # Verify all orthonormal
        for i, card_i in enumerate(cards):
            for j, card_j in enumerate(cards):
                inner = np.dot(card_i.T, card_j)[0, 0]
                if i == j:
                    assert np.isclose(inner, 1.0), "Cards should be normalized"
                else:
                    assert np.abs(inner) < 1e-10, "Cards should be orthogonal"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
