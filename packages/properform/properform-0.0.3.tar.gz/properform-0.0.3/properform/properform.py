# -*- coding: utf-8 -*-

import grpc
import marshal
from properform_pb2 import Profile
from properform_pb2_grpc import ProperformStub


def Push(addr, ID, profile):
	stats = marshal.load(open(profile, 'rb'))
	stub = ProperformStub(grpc.insecure_channel(addr))
	profile = Profile(ID = ID)
	for (f, l, n), (pc, rc, it, ct, callers) in stats.iteritems():
		callee = profile.Stats.add()
		callee.Function.File = f
		callee.Function.Line = l
		callee.Function.Name = n
		callee.Stat.PrimitiveCalls = pc
		callee.Stat.RecursiveCalls = rc
		callee.Stat.InternalTime = it
		callee.Stat.CumulativeTime = ct
		for (f, l, n), (pc, rc, it, ct) in callers.iteritems():
			caller = callee.Callers.add()
			caller.Function.File = f
			caller.Function.Line = l
			caller.Function.Name = n
			caller.Stat.PrimitiveCalls = pc
			caller.Stat.RecursiveCalls = rc
			caller.Stat.InternalTime = it
			caller.Stat.CumulativeTime = ct
	reply = stub.Push(profile)
	print "[Properform] Push ", reply.Success
