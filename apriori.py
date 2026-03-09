import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import random

np.random.seed(42)
random.seed(42)

class AprioriAlgorithm:
    def __init__(self, min_support=0.5, min_confidence=0.7):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = []
        self.association_rules = []
    
    def get_support(self, itemset, transactions):
        count = sum(1 for trans in transactions if itemset.issubset(trans))
        return count / len(transactions)
    
    def get_support_count(self, itemset, transactions):
        return sum(1 for trans in transactions if itemset.issubset(trans))
    
    def generate_candidates(self, prev_itemsets, k):
        candidates = set()
        prev_list = list(prev_itemsets)
        
        for i in range(len(prev_list)):
            for j in range(i + 1, len(prev_list)):
                union = prev_list[i] | prev_list[j]
                if len(union) == k:
                    is_valid = True
                    for item in union:
                        subset = union - {item}
                        if subset not in prev_itemsets:
                            is_valid = False
                            break
                    if is_valid:
                        candidates.add(union)
        
        return candidates
    
    def fit(self, transactions):
        transactions = [set(t) for t in transactions]
        n_transactions = len(transactions)
        
        all_items = set()
        for trans in transactions:
            all_items.update(trans)
        
        print(f"\nTotal transactions: {n_transactions}")
        print(f"Unique items: {sorted(all_items)}")
        
        current_itemsets = set()
        item_counts = {}
        
        for item in all_items:
            itemset = frozenset([item])
            support = self.get_support(itemset, transactions)
            if support >= self.min_support:
                current_itemsets.add(itemset)
                item_counts[itemset] = support
                print(f"  Frequent 1-itemset: {set(itemset)}, Support: {support:.3f}")
        
        self.frequent_itemsets.append(current_itemsets)
        
        k = 2
        while current_itemsets:
            print(f"\n--- Finding frequent {k}-itemsets ---")
            
            candidates = self.generate_candidates(current_itemsets, k)
            
            current_itemsets = set()
            for candidate in candidates:
                support = self.get_support(candidate, transactions)
                if support >= self.min_support:
                    current_itemsets.add(candidate)
                    print(f"  Frequent {k}-itemset: {set(candidate)}, Support: {support:.3f}")
            
            if current_itemsets:
                self.frequent_itemsets.append(current_itemsets)
            
            k += 1
        
        self.generate_association_rules(transactions)
        
        return self
    
    def generate_association_rules(self, transactions):
        print("\n" + "=" * 50)
        print("ASSOCIATION RULES")
        print("=" * 50)
        
        for itemsets in self.frequent_itemsets[1:]:
            for itemset in itemsets:
                if len(itemset) < 2:
                    continue
                
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        antecedent = frozenset(antecedent)
                        consequent = itemset - antecedent
                        
                        support_ab = self.get_support(itemset, transactions)
                        support_a = self.get_support(antecedent, transactions)
                        
                        if support_a > 0:
                            confidence = support_ab / support_a
                            
                            if confidence >= self.min_confidence:
                                support_b = self.get_support(consequent, transactions)
                                lift = confidence / support_b if support_b > 0 else 0
                                
                                rule = {
                                    'antecedent': set(antecedent),
                                    'consequent': set(consequent),
                                    'support': support_ab,
                                    'confidence': confidence,
                                    'lift': lift
                                }
                                self.association_rules.append(rule)
                                
                                print(f"  {set(antecedent)} -> {set(consequent)}")
                                print(f"    Support: {support_ab:.3f}, Confidence: {confidence:.3f}, Lift: {lift:.3f}")
        
        return self.association_rules
    
    def get_frequent_itemsets(self):
        result = []
        for level, itemsets in enumerate(self.frequent_itemsets, 1):
            for itemset in itemsets:
                result.append({
                    'itemset': set(itemset),
                    'length': level,
                    'support': self.get_support(itemset, [])
                })
        return result


def visualize_support(transactions, title, filename):
    item_counts = {}
    for trans in transactions:
        for item in trans:
            item_counts[item] = item_counts.get(item, 0) + 1
    
    items = sorted(item_counts.keys())
    counts = [item_counts[i] for i in items]
    supports = [c / len(transactions) for c in counts]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    colors = ['#667eea' if s >= 0.5 else '#764ba2' for s in supports]
    ax1.bar(items, counts, color=colors)
    ax1.set_xlabel('Items')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Item Frequencies in Transactions')
    ax1.axhline(y=len(transactions) * 0.5, color='r', linestyle='--', label='Min Support (50%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.pie(counts, labels=items, autopct='%1.1f%%', colors=colors)
    ax2.set_title('Item Distribution')
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {filename}")


print("\n" + "="*50)
print("EXAMPLE 1: Market Basket Analysis")
print("(Online Shopping Transactions)")
print("="*50)

shopping_transactions = [
    {'milk', 'bread', 'eggs'},
    {'bread', 'butter', 'eggs'},
    {'milk', 'bread', 'butter'},
    {'bread', 'eggs'},
    {'milk', 'eggs'},
    {'bread', 'milk', 'cheese'},
    {'eggs', 'butter', 'bread'},
    {'milk', 'bread', 'eggs', 'butter'},
    {'cheese', 'milk'},
    {'bread', 'cheese', 'butter'},
]

print("\nTransaction Database:")
for i, trans in enumerate(shopping_transactions, 1):
    print(f"  T{i}: {sorted(trans)}")

apriori = AprioriAlgorithm(min_support=0.4, min_confidence=0.6)
apriori.fit(shopping_transactions)

visualize_support(shopping_transactions, 
                  "A-Priori Algorithm - Market Basket Analysis\nItem Support Visualization",
                  "apriori_example1.png")


print("\n" + "="*50)
print("EXAMPLE 2: Student Course Selection Patterns")
print("="*50)

course_transactions = [
    {'Math', 'Physics', 'Chemistry'},
    {'Math', 'Computer Science', 'Physics'},
    {'Math', 'Statistics', 'Economics'},
    {'Physics', 'Chemistry', 'Biology'},
    {'Math', 'Computer Science', 'Statistics'},
    {'Computer Science', 'Math', 'Physics', 'Statistics'},
    {'Chemistry', 'Biology', 'Physics'},
    {'Math', 'Economics', 'Statistics'},
    {'Computer Science', 'Physics'},
    {'Math', 'Physics', 'Chemistry', 'Biology'},
    {'Economics', 'Statistics', 'Math'},
    {'Computer Science', 'Math'},
    {'Physics', 'Chemistry'},
    {'Math', 'Statistics', 'Computer Science'},
    {'Biology', 'Chemistry', 'Physics'},
]

print("\nStudent Course Enrollments:")
for i, trans in enumerate(course_transactions, 1):
    print(f"  Student {i}: {sorted(trans)}")

apriori2 = AprioriAlgorithm(min_support=0.35, min_confidence=0.7)
apriori2.fit(course_transactions)

visualize_support(course_transactions, 
                  "A-Priori Algorithm - Student Course Selection\nItem Support Visualization",
                  "apriori_example2.png")
