import musicbrainzngs


def album_search():
    musicbrainzngs.set_useragent('SWS_class_proj', '0.0', contact='kurtzma4@msu.edu')

    album_search = input("Search for an Album")

    result = musicbrainzngs.search_release_groups(album_search)
    search_dict = {}
    for i, album in enumerate(result['release-group-list']):
        if i == 51:
            break
        try:
            if album['primary-type'] == 'Album':
                search_dict[i] = album
                print(str(i) + ": " + u"{id} - {name}".format(id=album['title'], name=album['artist-credit'][0]['artist']['name']))
        except KeyError:
            pass

    return search_dict


if __name__ == '__main__':
    album_search()

