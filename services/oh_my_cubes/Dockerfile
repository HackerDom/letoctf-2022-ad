
FROM golang:1.18 as build


RUN apt-get update
RUN apt install -y protobuf-compiler protoc-gen-go

WORKDIR /app

ENV GO111MODULE=on
ENV CGO_ENABLED=0

COPY service service

WORKDIR /app/service
RUN go mod download
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

RUN make

FROM scratch

COPY --from=build /app/service/game_server/game_server .

ENTRYPOINT ["./game_server"]
