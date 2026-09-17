import csv


def load_top_rated(filename='imdb-top-rated.csv'):
    """Return a set of (title, year) tuples for movies in the top rated list."""
    top_rated = set()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            rank, title, year, rating = row
            top_rated.add((title, year))
    return top_rated


def load_top_grossing(filename='imdb-top-grossing.csv'):
    """Return a dict mapping (title, year) -> USA Box Office (int)."""
    top_grossing = {}
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            rank, title, year, box_office = row
            top_grossing[(title, year)] = int(box_office)
    return top_grossing


def load_casts(filename='imdb-top-casts.csv'):
    """Return a dict mapping (title, year) -> (director, [actors])."""
    casts = {}
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)  # no header row in this file
        for row in reader:
            title, year, director, *actors = row
            casts[(title, year)] = (director, actors)
    return casts


def display_top_collaborations(top_rated_file='imdb-top-rated.csv',
                               casts_file='imdb-top-casts.csv', limit=10):
    """
    Displays (director, actor, number of movies) tuples for movies that
    are both in the top rated list and have cast info available, ordered
    by descending number of movies that director and actor worked
    together on. Ties may appear in any order. Only the top `limit`
    results are printed; pass limit=None to print all of them.
    """
    top_rated = load_top_rated(top_rated_file)
    casts = load_casts(casts_file)

    collaborations = {}
    for (title, year) in top_rated:
        if (title, year) in casts:
            director, actors = casts[(title, year)]
            for actor in actors:
                if actor:
                    key = (director, actor)
                    collaborations[key] = collaborations.get(key, 0) + 1

    results = [(director, actor, count)
               for (director, actor), count in collaborations.items()]
    results.sort(key=lambda x: x[2], reverse=True)

    for director, actor, count in results[:limit]:
        print(f"{director} - {actor}: {count}")
    if limit is not None and len(results) > limit:
        print(f"... ({len(results) - limit} more not shown)")

    return results


def display_top_actors(top_grossing_file='imdb-top-grossing.csv',
                       casts_file='imdb-top-casts.csv', limit=10):
    """
    Displays a ranking of actors from the top grossing list, ordered by
    descending total USA box office of the movies (in that list, with
    known cast info) they acted in. Only the top `limit` results are
    printed; pass limit=None to print all of them.
    """
    top_grossing = load_top_grossing(top_grossing_file)
    casts = load_casts(casts_file)

    actor_totals = {}
    for (title, year), box_office in top_grossing.items():
        if (title, year) in casts:
            director, actors = casts[(title, year)]
            for actor in actors:
                if actor:
                    actor_totals[actor] = actor_totals.get(actor, 0) + box_office

    results = [(actor, total) for actor, total in actor_totals.items()]
    results.sort(key=lambda x: x[1], reverse=True)

    for actor, total in results[:limit]:
        print(f"{actor}: ${total:,}")
    if limit is not None and len(results) > limit:
        print(f"... ({len(results) - limit} more not shown)")

    return results


def main():
    """Runs and sanity-checks both functions against the IMDB CSV files."""

    print("=" * 60)
    print("TOP DIRECTOR-ACTOR COLLABORATIONS (top rated movies)")
    print("=" * 60)
    collab_results = display_top_collaborations()

    # Basic sanity checks: correct types, and list is sorted descending.
    assert all(isinstance(t, tuple) and len(t) == 3 for t in collab_results), \
        "Each result should be a (director, actor, count) tuple"
    counts = [count for _, _, count in collab_results]
    assert counts == sorted(counts, reverse=True), \
        "Collaboration results should be sorted in descending order"
    print(f"\n[OK] {len(collab_results)} director-actor pairs found, "
          f"correctly sorted descending.")
    print(f"[OK] Top collaboration: {collab_results[0]}")

    print()
    print("=" * 60)
    print("TOP ACTORS BY BOX OFFICE (top grossing movies)")
    print("=" * 60)
    actor_results = display_top_actors()

    assert all(isinstance(t, tuple) and len(t) == 2 for t in actor_results), \
        "Each result should be an (actor, total_box_office) tuple"
    totals = [total for _, total in actor_results]
    assert totals == sorted(totals, reverse=True), \
        "Actor results should be sorted in descending order"
    print(f"\n[OK] {len(actor_results)} actors found, correctly sorted descending.")
    print(f"[OK] Top actor: {actor_results[0]}")

    print()
    print("All checks passed.")


if __name__ == '__main__':
    main()