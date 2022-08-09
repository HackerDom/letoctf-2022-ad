package main

import (
	"context"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"summer-2022/auth"
	"summer-2022/proto"
)

type Client struct {
	authClient proto.AuthClient
	omcClient  proto.OMCClient
	authInfo   *proto.AuthInfo
	lg         *zap.Logger
}

func (c *Client) CreateRealm(ctx context.Context) error {
	//TODO implement me
	panic("implement me")
}

func (c *Client) GetRealm(ctx context.Context, in *proto.RealmId) (*proto.Realm, error) {
	//TODO implement me
	panic("implement me")
}

func (c *Client) GetState(ctx context.Context) (*proto.State, error) {
	return c.omcClient.GetState(c.getAuthContext(ctx), &proto.Empty{})
}

func (c *Client) getAuthContext(ctx context.Context) context.Context {
	header := metadata.New(map[string]string{auth.JWT_METADATA: c.authInfo.Token})
	return metadata.NewOutgoingContext(ctx, header)
}

func (c *Client) SendAction(ctx context.Context, in *proto.Action) (*proto.State, error) {
	return c.omcClient.SendAction(c.getAuthContext(ctx), in)
}

func NewClient(target string, authTarget string, lg *zap.Logger) Client {
	authClient := proto.NewAuthClient(getConnection(authTarget, lg))
	omcClient := proto.NewOMCClient(getConnection(target, lg))
	return Client{
		authClient: authClient,
		omcClient:  omcClient,
		lg:         lg,
	}
}

func getConnection(target string, lg *zap.Logger) *grpc.ClientConn {
	dial, err := grpc.Dial(target, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		lg.Fatal("Can't connect", zap.Error(err))
	}
	return dial
}

func (c *Client) SignIn(ctx context.Context, login string, password string) error {
	authInfo, err := c.authClient.SignIn(ctx, &proto.UserInfo{
		Login:    login,
		Password: password,
	})

	if err != nil {
		return err
	}

	c.authInfo = authInfo
	c.lg.Info("--> login as: " + login)

	return nil
}
