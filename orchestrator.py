from agent import Agent

class Orchestrator:

    def __init__(self, llm_config:dict):
        agent = Agent(llm_config)
        self.writer = agent.get_writer()
        self.critic = agent.get_critic()
        self.SEO_reviewer = agent.get_SEO_reviewer()
        self.legal_reviewer = agent.get_legal_reviewer()
        self.ethics_reviewer = agent.get_ethics_reviewer()
        self.meta_reviewer = agent.get_meta_reviewer()

    def get_nested_chats(self, max_turns:int=1):
        def reflection_message(recipient, sender):
            return f'''Review the following content. 
                \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

        nested_chats = [
            {
                "recipient": self.SEO_reviewer, 
                "message": reflection_message, 
                "summary_method": "reflection_with_llm",
                "summary_args": {"summary_prompt" : 
                    "Return review into as JSON object only:"
                    "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",},
                "max_turns": max_turns
            },
            {
                "recipient": self.legal_reviewer, "message": reflection_message, 
                "summary_method": "reflection_with_llm",
                "summary_args": {"summary_prompt" : 
                    "Return review into as JSON object only:"
                    "{'Reviewer': '', 'Review': ''}.",},
                "max_turns": max_turns
            },
            {
                "recipient": self.ethics_reviewer, "message": reflection_message, 
                "summary_method": "reflection_with_llm",
                "summary_args": {"summary_prompt" : 
                    "Return review into as JSON object only:"
                    "{'reviewer': '', 'review': ''}",},
                "max_turns": max_turns
            },
            {
                "recipient": self.meta_reviewer, 
                "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
                "max_turns": max_turns
            },
        ]
        return nested_chats
    
    def register_nested_chats(self, max_turns:int=1):
        return self.critic.register_nested_chats(
            self.get_nested_chats(max_turns),
            trigger=self.writer(),
        )
    
    def generate_response(self, task:str, max_turns:int=1):
        self.register_nested_chats(max_turns)
        response = self.critic.initiate_chat(
            recipient=self.writer,
            message=task,
            max_turns=max_turns+1,
            summary_method="last_msg"
        )
        return response

    def get_writer_responses(self, response:object):
        writer_responses = []
        for chat in response.chat_history:
            if chat["name"] == "Writer":
                writer_responses.append(chat["content"])
        return writer_responses
    
    def get_meta_feedback(self, response:object):
        critic_responses = []
        for chat in response.chat_history:
            if chat["name"] == "Critic":
                critic_responses.append(chat["content"])
        return critic_responses[-1]
    
    def get_cost(self, response:object):
        cost = response.cost
        total_cost = round(cost["usage_including_cached_inference"]["total_cost"], 4)
        cost_non_cached = round(cost["usage_excluding_cached_inference"]["total_cost"], 4)
        return {"total_cost": total_cost, "cost_non_cached": cost_non_cached}
    