package main

import (
	"context"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"io"
	"summer-2022/auth"
	"summer-2022/proto"
)

type Client struct {
	authClient proto.AuthClient
	omcClient  proto.OMCClient
	authInfo   *proto.AuthInfo
	lg         *zap.Logger
}

func (c *Client) PutBlock(ctx context.Context, block *proto.Block) error {
	_, err := c.omcClient.PutBlock(c.getAuthContext(ctx), block)
	if err != nil {
		return err
	}

	return nil
}

func (c *Client) GetBlocks(ctx context.Context) ([]*proto.Block, error) {
	resp, err := c.omcClient.GetBlocks(c.getAuthContext(ctx), &proto.Empty{})
	if err != nil {
		return nil, err
	}

	var blocks []*proto.Block

	for {
		recv, err := resp.Recv()

		if err != nil {
			if err == io.EOF {
				break
			}

			return nil, err
		}
		blocks = append(blocks, recv)
	}

	return blocks, nil
}

func (c *Client) PutShared(ctx context.Context, in *proto.Block) (*proto.SharedBlockCreateResponse, error) {
	return c.omcClient.PutShared(c.getAuthContext(ctx), in)
}

func (c *Client) GetShared(ctx context.Context, in *proto.GetSharedBlock) (*proto.SharedBlock, error) {
	return c.omcClient.GetShared(c.getAuthContext(ctx), in)
}

func (c *Client) GetSharedList(ctx context.Context) ([]string, error) {
	list, err := c.omcClient.GetSharedList(ctx, &proto.Empty{})
	if err != nil {
		return nil, err
	}

	return list.Ids, nil
}

func (c *Client) getAuthContext(ctx context.Context) context.Context {
	header := metadata.New(map[string]string{auth.METADATA_KEY: c.authInfo.Token})
	return metadata.NewOutgoingContext(ctx, header)
}

func NewClient(ctx context.Context, target string, authTarget string, lg *zap.Logger) (*Client, error) {
	connection, err := getConnection(ctx, authTarget, lg)
	if err != nil {
		return nil, err
	}
	authClient := proto.NewAuthClient(connection)
	conn, err := getConnection(ctx, target, lg)
	if err != nil {
		return nil, err
	}
	omcClient := proto.NewOMCClient(conn)
	return &Client{
		authClient: authClient,
		omcClient:  omcClient,
		lg:         lg,
	}, nil
}

func getConnection(ctx context.Context, target string, lg *zap.Logger) (*grpc.ClientConn, error) {
	dial, err := grpc.DialContext(ctx, target, grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock(), grpc.FailOnNonTempDialError(true))
	if err != nil {
		return nil, err
	}
	return dial, nil
}

func (c *Client) SignUp(ctx context.Context, login string) error {
	authInfo, err := c.authClient.SignUp(ctx, &proto.UserInfo{
		Login: login,
	})

	if err != nil {
		return err
	}

	c.authInfo = authInfo
	c.lg.Info("--> login as: " + login)

	return nil
}

func (c *Client) SetAuth(authInfo *proto.AuthInfo) {
	c.authInfo = authInfo
}
