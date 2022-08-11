package main

import (
	"context"
	"encoding/json"
	"fmt"
	"go.uber.org/zap"
	"summer-2022/proto"
	"time"
)

const (
	OK            = 101
	CORRUPT       = 102
	MUMBLE        = 103
	DOWN          = 104
	CHECKER_ERROR = 110
)

var timeout = time.Second * 1

type V1FlagId struct {
	Auth  *proto.AuthInfo `json:"Auth,omitempty"`
	Block *proto.Block    `json:"Block,omitempty"`
}

type V2FlagId struct {
	Auth     *proto.AuthInfo                  `json:"Auth,omitempty"`
	Response *proto.SharedBlockCreateResponse `json:"Response,omitempty"`
	Block    *proto.Block                     `json:"Block,omitempty"`
}

type Checker struct {
	lg   *zap.Logger
	host string
}

func (c *Checker) Check() {
	c.Put1("test")

}

func (c *Checker) Put1(data string) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	client, ok := c.TryConnect(ctx)
	if !ok {
		Verdict(DOWN, "")
		return
	}

	err := client.SignUp(ctx, "bob")
	if err != nil {
		c.lg.Error(err.Error())
		Verdict(MUMBLE, err.Error())
		return
	}

	block := &proto.Block{
		Name:        "Block name",
		SecretNotes: data,
	}
	err = client.PutBlock(ctx, block)
	if err != nil {
		c.lg.Error(err.Error())
		Verdict(MUMBLE, err.Error())
		return
	}

	flagId := V1FlagId{
		Auth:  client.authInfo,
		Block: block,
	}

	marshal, err := json.Marshal(flagId)
	if err != nil {
		Verdict(CHECKER_ERROR, err.Error())
		return
	}

	Verdict(OK, string(marshal))
}

func (c *Checker) Get1(data string) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	client, ok := c.TryConnect(ctx)
	if !ok {
		Verdict(DOWN, "")
		return
	}

	var flagId V1FlagId
	err := json.Unmarshal([]byte(data), &flagId)
	if err != nil {
		Verdict(CHECKER_ERROR, err.Error())
		return
	}

	client.SetAuth(flagId.Auth)

	blocks, err := client.GetBlocks(ctx)
	if err != nil {
		Verdict(MUMBLE, err.Error())
		return
	}

	for _, block := range blocks {
		if block.SecretNotes == flagId.Block.SecretNotes {
			if block.Name != flagId.Block.Name {
				Verdict(MUMBLE, "invalid name")
			}

			Verdict(OK, "ok")
			return
		}
	}

	Verdict(CORRUPT, "Block not found")
}

func (c *Checker) Put2(data string) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	client, ok := c.TryConnect(ctx)
	if !ok {
		Verdict(DOWN, "down")
		return
	}

	err := client.SignUp(ctx, "bob")
	if err != nil {
		c.lg.Error(err.Error())
		Verdict(MUMBLE, err.Error())
		return
	}

	block := &proto.Block{
		Name:        "Block name",
		SecretNotes: data,
	}
	resp, err := client.PutShared(ctx, block)
	if err != nil {
		c.lg.Error(err.Error())
		Verdict(MUMBLE, err.Error())
		return
	}

	flagId := V2FlagId{
		Auth:     client.authInfo,
		Response: resp,
		Block:    block,
	}

	marshal, err := json.Marshal(flagId)
	if err != nil {
		Verdict(CHECKER_ERROR, err.Error())
		return
	}

	Verdict(OK, string(marshal))
}

func (c *Checker) Get2(data string) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	client, ok := c.TryConnect(ctx)
	if !ok {
		Verdict(DOWN, "down")
		return
	}

	var flagId V2FlagId
	err := json.Unmarshal([]byte(data), &flagId)
	if err != nil {
		Verdict(CHECKER_ERROR, err.Error())
		return
	}

	c.lg.Info("recived ", zap.Reflect("falg_id", flagId))

	client.SetAuth(flagId.Auth)

	block, err := client.GetShared(ctx, &proto.GetSharedBlock{
		SharedId: flagId.Response.Metadata.SharedId,
		AdminKey: flagId.Response.AdminKey,
	})
	if err != nil {
		Verdict(CORRUPT, err.Error())
		return
	}

	c.lg.Info("get", zap.Reflect("block", block))

	if block.Block.SecretNotes != flagId.Block.SecretNotes {
		Verdict(CORRUPT, "Can't get flag")
		return
	}

	if block.Block.Name != flagId.Block.Name {
		Verdict(MUMBLE, "Can't find name")
		return
	}

	Verdict(101, "ok")
}

func (c *Checker) TryConnect(ctx context.Context) (*Client, bool) {
	authTarget := fmt.Sprintf("%s:8090", c.host)
	omcTarget := fmt.Sprintf("%s:9090", c.host)
	client, err := NewClient(ctx, omcTarget, authTarget, c.lg)
	if err != nil {
		c.lg.Error(err.Error())
		Verdict(DOWN, err.Error())
		return nil, false
	}
	return client, true
}

func Verdict(code int, reason string) {
	fmt.Println(fmt.Sprintf("VERDICT_CODE:%d", code))

	if reason == "" {
		reason = "-"
	}
	fmt.Println(fmt.Sprintf("VERDICT_REASON:%s", reason))
}
