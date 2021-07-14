import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probdistribution= dict()
    # if page has at least one link leading to another page
    if corpus[page]:
        for link in corpus:
            probdistribution[link]= (1-damping_factor)/len(corpus) # randomly choose page out of pages in corpus
            if link in corpus[page]:
                probdistribution[link]=probdistribution[link] + damping_factor/len(corpus[page]) # Include additional probability for pages linked to by current page
    else:
        # if there is no outgoing link, choose randomly among all pages with equal probability. 
        for link in corpus:
            probdistribution[link]=1/len(corpus)
    return probdistribution


    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    PageRank= dict()
    for page in corpus:
        PageRank[page]=0
    
    # generate 1st sample by choosing from a page at random
    sample_space= random.choice(list(corpus.keys()))
    
    # Sampling n pages(including the generation of first sample)
    for iteration in range(n-1):
        
        transition= transition_model(corpus, sample_space, damping_factor )
        sample_space=random.choices(list(transition.keys()), transition.values())[0]
        PageRank[sample_space]=PageRank[sample_space]+1 
    
    # Normalising the PageRank values
    for page in corpus:
        PageRank[page]= PageRank[page]/n
    return PageRank


   # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank= dict()
    UpdatedRank= dict()
    # Initialising values for PageRank
    for page in corpus:
        PageRank[page]=1/len(corpus)
    
    continueProcess= True

    while continueProcess:
        for page in PageRank:
            sum= float(0)

            for every_page in corpus: 
                # Every page that links to current page must be considered
                if page in corpus[every_page]:
                    sum= sum+ PageRank[every_page]/len(corpus[every_page])
                # Page with no links is considered to have 1 link for every page(including itself)
                if not corpus[every_page]:
                    sum= sum+ PageRank[every_page]/len(corpus)

            UpdatedRank[page]= damping_factor*sum + (1-damping_factor)/len(corpus)
        

        # Keep a tab if the values change by more than 0.001
        for page in PageRank:
            if math.isclose(UpdatedRank[page], PageRank[page], abs_tol=0.001):
                continueProcess=False
            else:
                continueProcess=True
            PageRank[page]= UpdatedRank[page]
    return PageRank



    # raise NotImplementedError


if __name__ == "__main__":
    main()
