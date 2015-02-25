import requests
class API:
    def media__mediaId__get(_,mediaId):
        url='/media/%s'%(mediaId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def media__mediaId__comments_get(_,mediaId):
        url='/media/%s/commnts'%(mediaId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def media__mediaId__comments_post(_,mediaId):
        url='/media/%s/comments'%(mediaId)
        print "URL:", url
        ret = requests.post(url)
        return ret
    def media__mediaId__comments__commentId__delete(_,mediaId,commentId):
        url='/media/%s/comments/%s'%(mediaId,commentId)
        print "URL:", url
        ret = requests.delete(url)
        return ret
    def media__mediaId__likes_delete(_,mediaId):
        url='/media/%s/likes'%(mediaId)
        print "URL:", url
        ret = requests.delete(url)
        return ret
    def media__mediaId__likes_post(_,mediaId):
        url='/media/%s/likes'%(mediaId)
        print "URL:", url
        ret = requests.post(url)
        return ret
    def media__mediaId__likes_get(_,mediaId):
        url='/media/%s/likes'%(mediaId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def media_search_get(_):
        url='/media/search'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def media_popular_get(_):
        url='/media/popular'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def tags__tagName__get(_,tagName):
        url='/tags/%s'%(tagName)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def tags__tagName__media_recent_get(_,tagName):
        url='/tags/%s/media/recent'%(tagName)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def tags_search_get(_):
        url='/tags/search'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users__userId__get(_,userId):
        url='/users/%s'%(userId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users__userId__follows_get(_,userId):
        url='/users/%s/follows'%(userId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users__userId__followed_by_get(_,userId):
        url='/users/%s/followed-by'%(userId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users__userId__requested_by_get(_,userId):
        url='/users/%s/requested-by'%(userId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users__userId__media_recent_get(_,userId):
        url='/users/%s/media/recent'%(userId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users__userId__relationship_post(_,userId):
        url='/users/%s/relationship'%(userId)
        print "URL:", url
        ret = requests.post(url)
        return ret
    def users__userId__relationship_get(_,userId):
        url='/users/%s/relationship'%(userId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users_search_get(_,userId):
        url='/users/search'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users_self_get(_,userId):
        url='/users/self'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users_self_feed_get(_):
        url='/users/self/feed'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def users_self_media_liked_get(_):
        url='/users/self/media/liked'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def oembed_get(_):
        url='/oembed'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def p__shortcode__media_get(_,shortcode):
        url='/p/%s/media'%(shortcode)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def locations__locId__get(_,locId):
        url='/locations/%s'%(locId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def locations__locId__media_recent_get(_,locId):
        url='/locations/%s/media/recent'%(locId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    def locations_search_get(_):
        url='/locations/search'
        print "URL:", url
        ret = requests.get(url)
        return ret
    def geographies__geoId__media_recent_get(_,geoId):
        url='/geographies/%s/media/recent'%(geoId)
        print "URL:", url
        ret = requests.get(url)
        return ret
    pass
api=API()

