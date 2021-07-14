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
    prob=1
    for person in people:
        if person in two_genes:
            gene=2
        elif person in one_gene:
            gene=1
        else:
            gene=0
        mother= people[person]["mother"]
        father= people[person]["father"]
        trait=person in have_trait

        # If no parents, apply unconditional probability
        if mother is None and father is None:
            prob=prob*PROBS["gene"][gene]
        else:
            pass_down={mother:0, father:0}
            
            for parent in pass_down:
                if parent in two_genes:
                    # chances of passing down stand 100% unless the gene mutates
                    pass_down[parent]=1-PROBS["mutation"]
                elif parent in one_gene:
                    # probability of passing down stand 0.5
                    pass_down[parent]=0.5
                else:
                    # Mutation is the only path
                    pass_down[parent]=PROBS["mutation"]
            if gene==2:
                prob= prob*pass_down[mother]*pass_down[father]
            elif gene==1:
                prob= prob*(pass_down[mother]*(1-pass_down[father])+ pass_down[father]*(1-pass_down[mother])) 
            else:
                prob=prob*(1-pass_down[mother])*(1-pass_down[father])           
        # Taking into account the factor of trait
        prob=prob*PROBS["trait"][gene][trait]
    return prob    

    # raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            gene=2
        elif person in one_gene:
            gene=1
        else:
            gene=0
       
        trait=person in have_trait
        probabilities[person]["gene"][gene]=probabilities[person]["gene"][gene] + p
        probabilities[person]["trait"][trait]=probabilities[person]["trait"][trait] + p 
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for gene_trait in probabilities[person]:
            number_gene_trait= sum(probabilities[person][gene_trait].values())
            for genes_traits in probabilities[person][gene_trait]:
                probabilities[person][gene_trait][genes_traits]/=number_gene_trait
    # raise NotImplementedError


if __name__ == "__main__":
    main()
