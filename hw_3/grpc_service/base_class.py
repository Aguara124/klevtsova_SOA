import grpc

from grpc_files import Posts_pb2, Posts_pb2_grpc
import db.db_posts as db_posts

class SocialNetworkServiceServicer(Posts_pb2_grpc.SocialNetworkServiceServicer):
    def CreatePost(self, request, context):
        tags = request.tags
        new_id = db_posts.create_post(request.title, request.creator_id, request.is_private, request.description, tags)
        print("Created new post ", new_id, " ", request.title)
        return Posts_pb2.CreatePostResponse(post_id=new_id, message="New post created")

    def UpdatePost(self, request, context):
        update = db_posts.update_post(request.post_id, request.title, request.description, request.tags, request.is_private)
        if update == True:
            return Posts_pb2.UpdatePostResponse(post_id=request.post_id, message="Post was updated")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Post not found')
        return Posts_pb2.UpdatePostResponse()
    
    def DeletePost(self, request, context):
        del_p = db_posts.delete_post(request.post_id)
        if del_p == True:
            return Posts_pb2.DeletePostResponse(post_id=request.post_id)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Post not found')
        return Posts_pb2.DeletePostResponse()

    def GetPostById(self, request, context):
        get_p = db_posts.get_post_by_id(request.post_id)
        if get_p == False:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Post not found')
            return Posts_pb2.GetPostByIdResponse()
        post_f = Posts_pb2.Post(
            id=get_p['id'],
            title = get_p['title'],
            creator_id = get_p['creator_id'],
            is_private = get_p['is_private'], 
            description = get_p['description'], 
            tags = get_p['tags'],
            creation_date = get_p['creation_date'],
            update_date = get_p['update_date']
        )
        return Posts_pb2.GetPostByIdResponse(post=post_f)

    def GetPostsList(self, request, context):
        arr = db_posts.get_posts_list()
        posts_arr = []
        for get_p in arr:
            post_f = Posts_pb2.Post(
                id=get_p['id'],
                title = get_p['title'],
                creator_id = get_p['creator_id'],
                is_private = get_p['is_private'], 
                description = get_p['description'], 
                tags = get_p['tags'],
                creation_date = get_p['creation_date'],
                update_date = get_p['update_date']
            )
            posts_arr.append(post_f)
        return posts_arr