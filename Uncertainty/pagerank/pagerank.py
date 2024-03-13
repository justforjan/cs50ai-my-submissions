import os
import random
import re
import sys
import copy

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

    transition_proba = {}

    # 1 - damping factor
    damping_proba = round((1 - damping_factor) / len(corpus), 2)

    for site in corpus:
        transition_proba[site] = damping_proba
    
    for linked_site in corpus[page]:
        transition_proba[linked_site] += round(damping_factor / len(corpus[page]), 2)
    
    return transition_proba


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    return_dict = {}

    for site in corpus:
        return_dict[site] = 0

    current_page = random.choice(list(corpus.keys()))

    c = 0

    while c < n:
        return_dict[current_page] += 1
        transitions = transition_model(corpus, current_page, DAMPING)
        current_page = random.choices(list(transitions.keys()), weights=list(transitions.values()), k=1)[0]
        c += 1

    for page in return_dict:
        return_dict[page] /= n

    return return_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    def numLinks(previous_page):
        return len(corpus[previous_page])
    

    def previous_pr(previous_page):
        return return_dict[previous_page]
    

    total_nr_of_pages = len(corpus)

    # Initiation of the ranks
    return_dict = {}
    for site in corpus:
        return_dict[site] = 1 / total_nr_of_pages
    
    # Interating over it  
    still_changing = True   
    while still_changing:
        still_changing = False

    # for n in range(10000):


        temp_results = copy.copy(return_dict)

        for site in return_dict:


            temp_results[site] = (1 - damping_factor) / total_nr_of_pages + damping_factor * (sum([previous_pr(page) / numLinks(page) if site in corpus[page] else previous_pr(page) / total_nr_of_pages if numLinks(page) == 0 else 0 for page in corpus ]))

        
        for page in return_dict:
            if abs(return_dict[page] - temp_results[page]) >= 0.001:
                still_changing = True
                break

        return_dict = temp_results

    return return_dict


if __name__ == "__main__":
    main()
