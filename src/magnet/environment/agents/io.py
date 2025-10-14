#!/usr/bin/env python
# -*- coding: utf-8 -*-

from magnet.graph import Graph
from magnet.environment.operations import DirectAnswer
from magnet.environment.agents.agent_registry import AgentRegistry


@AgentRegistry.register('IO')
class IO(Graph):
    def build_graph(self):
        io = DirectAnswer(self.domain, self.model_name)
        self.add_node(io)
        self.input_nodes = [io]
        self.output_nodes = [io]
