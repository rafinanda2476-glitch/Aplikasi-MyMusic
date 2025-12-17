# fuzzy search - pake yg simpel aja
def fuzzy_search_songs(query,songs,threshold=2,search_fields=None):
    res=[];q=query.lower();[res.append(s) for s in songs if q in s.title.lower() or q in s.artist.lower()];return res
