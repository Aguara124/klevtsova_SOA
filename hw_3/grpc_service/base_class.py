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
        if update == "Incorrect input.":
            return Posts_pb2.UpdatePostResponse(post_id=request.post_id, message="Incorrect input. You should use only letters and digits.")
        if update == True:
            return Posts_pb2.UpdatePostResponse(post_id=request.post_id, message="Post was updated")
        return Posts_pb2.UpdatePostResponse(post_id=request.post_id, message="Post was not found")
    
    def DeletePost(self, request, context):
        del_p = db_posts.delete_post(request.post_id)
        if del_p == True:
            return Posts_pb2.DeletePostResponse(post_id=request.post_id, message="Post was deleted")
        return Posts_pb2.DeletePostResponse(post_id=request.post_id, message="Post was not found")

    def GetPostById(self, request, context):
        get_p = db_posts.get_post_by_id(request.post_id)
        print(get_p)
        if get_p == None:
            print("Post not found")
            post_f = Posts_pb2.Post(
                id=0,
                title = 'No',
                creator_id = 0,
                is_private = False, 
                description = 'No', 
                tags = 'No',
                creation_date = 'No',
                update_date = 'No'
            )
            return Posts_pb2.GetPostByIdResponse(post=post_f)
        post_f = Posts_pb2.Post(
            id=int(get_p[0]),
            title = get_p[1],
            creator_id = int(get_p[3]),
            is_private = bool(get_p[6]), 
            description = get_p[2], 
            tags = get_p[7],
            creation_date = str(get_p[4]),
            update_date = str(get_p[5])
        )
        print("Here 4")
        return Posts_pb2.GetPostByIdResponse(post=post_f)

    def GetPostsList(self, request, context):
        arr = db_posts.get_posts_list()
        posts_arr = []
        for get_p in arr:
            post_f = Posts_pb2.Post(
                id=int(get_p[0]),
                title = get_p[1],
                creator_id = int(get_p[3]),
                is_private = bool(get_p[6]), 
                description = get_p[2], 
                tags = get_p[7],
                creation_date = str(get_p[4]),
                update_date = str(get_p[5])
            )
            posts_arr.append(post_f)
        return Posts_pb2.GetPostsListResponse(posts = posts_arr)