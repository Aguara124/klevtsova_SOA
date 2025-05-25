from user_services.user_service import router as user_router
from grpc_service.posts_service import router as posts_router
from statistics_files.stats_proxy import router as stat_router
from fastapi import FastAPI
from fastapi.testclient import TestClient
import grpc
from concurrent import futures
import time

from grpc_service.base_class import SocialNetworkServiceServicer
from grpc_files import Posts_pb2, Posts_pb2_grpc

from technical_files.protos.generated import stats_pb2_grpc, stats_pb2
from statistics_files.stats_server import StatisticsService
app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Проект Клевцовой Снежаны 221"}

app.include_router(user_router)
app.include_router(posts_router)
app.include_router(stat_router)

client = TestClient(app)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
Posts_pb2_grpc.add_SocialNetworkServiceServicer_to_server(SocialNetworkServiceServicer(), server)
stats_pb2_grpc.add_StatisticsServiceServicer_to_server(StatisticsService(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("gRPC Master Book Service запущен на порту 50051...")
# try:
#     while True:
#         time.sleep(86400)
# except KeyboardInterrupt:
#     server.stop(0)
