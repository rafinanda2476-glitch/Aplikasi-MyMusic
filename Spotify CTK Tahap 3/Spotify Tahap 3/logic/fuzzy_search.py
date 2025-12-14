# logic/fuzzy_search.py
"""
Fuzzy string matching using Levenshtein distance algorithm.
Allows typo-tolerant search functionality.
"""

def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.
    Returns the minimum number of single-character edits (insertions, deletions, or substitutions)
    required to change one string into the other.
    """
    s1 = s1.lower()
    s2 = s2.lower()
    
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def fuzzy_match(query, target, threshold=2):
    """
    Check if query matches target within the given edit distance threshold.
    
    Args:
        query: The search query string
        target: The target string to match against
        threshold: Maximum edit distance to consider a match (default: 2)
    
    Returns:
        True if the strings match within threshold, False otherwise
    """
    # Exact match or substring match always returns True
    query_lower = query.lower()
    target_lower = target.lower()
    
    if query_lower in target_lower or target_lower in query_lower:
        return True
    
    # Calculate edit distance
    distance = levenshtein_distance(query, target)
    return distance <= threshold


def fuzzy_search_songs(query, songs, threshold=2, search_fields=['title', 'artist']):
    """
    Search songs using fuzzy matching on specified fields.
    
    Args:
        query: The search query string
        songs: List of Song objects to search
        threshold: Maximum edit distance for fuzzy matching (default: 2)
        search_fields: List of fields to search ['title', 'artist', 'genre']
    
    Returns:
        List of matching Song objects, sorted by relevance
    """
    if not query or not songs:
        return []
    
    matches = []
    query_lower = query.lower()
    
    for song in songs:
        matched = False
        exact_match = False
        
        # Check each field
        for field in search_fields:
            field_value = getattr(song, field, "")
            field_lower = field_value.lower()
            
            # Exact or substring match (highest priority)
            if query_lower in field_lower or field_lower in query_lower:
                exact_match = True
                matched = True
                break
            
            # Fuzzy match (lower priority)
            if fuzzy_match(query, field_value, threshold):
                matched = True
        
        if matched:
            # Add tuple: (song, priority) where exact matches have priority 0
            matches.append((song, 0 if exact_match else 1))
    
    # Sort by priority (exact matches first), then by song title
    matches.sort(key=lambda x: (x[1], x[0].title))
    
    return [song for song, _ in matches]


def get_similar_words(word, word_list, threshold=2, max_results=5):
    """
    Find similar words from a word list based on Levenshtein distance.
    Useful for suggesting corrections.
    
    Args:
        word: The word to find similar matches for
        word_list: List of words to search
        threshold: Maximum edit distance (default: 2)
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        List of tuples (word, distance) sorted by distance
    """
    results = []
    
    for candidate in word_list:
        distance = levenshtein_distance(word, candidate)
        if distance <= threshold:
            results.append((candidate, distance))
    
    # Sort by distance, then alphabetically
    results.sort(key=lambda x: (x[1], x[0]))
    
    return results[:max_results]
