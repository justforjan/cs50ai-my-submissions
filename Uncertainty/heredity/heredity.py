import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    def nr_of_genes_proba(person_genes, has_parent, mother_genes, father_genes):

        # has no parents:
        if has_parent is None:
            return PROBS['gene'][person_genes]
        
        # has parents:
        else:
            probability = 1

            # person has no genes
            if person_genes == 0:
                # not from mother and not from fater
                probability *= proba_genes_from_parent(mother_genes, False)
                probability *= proba_genes_from_parent(father_genes, False)
    
            elif person_genes == 1:
                # from mother and not from fater
                probability *= proba_genes_from_parent(mother_genes, True)
                probability *= proba_genes_from_parent(father_genes, False)
            
                # not from mother and from father
                p = 1
                p *= proba_genes_from_parent(mother_genes, False)
                p *= proba_genes_from_parent(father_genes, True)

                probability += p

            else: 
                # from father and from mother
                probability *= proba_genes_from_parent(mother_genes, True)
                probability *= proba_genes_from_parent(father_genes, True)
    
        return probability
            

    def proba_genes_from_parent(parent_genes, gets_gene_from_this_parent):

        if gets_gene_from_this_parent:
            if parent_genes == 0:
                return PROBS['mutation']
            elif parent_genes == 1:
                p = 0.5 * (1-PROBS['mutation']) # gets gene from parent and gene it not mutated
                p += 0.5 * PROBS['mutation'] # does not get gene from parent but gene gets mutated
                return p
            else:
                return 1-PROBS['mutation']
            
        else:
            if parent_genes == 0:
                return 1-PROBS['mutation']
            elif parent_genes == 1:
                p = 0.5 * (1-PROBS['mutation']) # does not get gene from parent and gene is not muated
                p += 0.5 * PROBS['mutation'] # gets gene from parent but gene gets mutated
                return p
            else:
                return PROBS['mutation']
    

    def proba_trait(person_genes, has_trait):
        return PROBS["trait"][person_genes][has_trait]


    # setting initial probability to one
    probability = 1

    for person in people:

        # probability of copies of the gene
        mother = people[person]['mother']
        father = people[person]['father']

        person_genes = 1 if person in one_gene else 2 if person in two_genes else 0
        mother_genes = 1 if mother in one_gene else 2 if mother in two_genes else 0
        father_genes = 1 if father in one_gene else 2 if father in two_genes else 0

        probability *= nr_of_genes_proba(person_genes, mother, mother_genes, father_genes)

        # probability of trait
        probability *= proba_trait(person_genes, person in have_trait)
    
    return probability

        

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p

        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        sum_gene = sum(list(probabilities[person]['gene'].values()))
        sum_trait = sum(list(probabilities[person]['trait'].values()))

        for i in range(3):
            probabilities[person]['gene'][i] /= sum_gene
        
        probabilities[person]['trait'][True] /= sum_trait
        probabilities[person]['trait'][False] /= sum_trait
    

if __name__ == "__main__":
    main()
