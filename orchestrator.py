from agent import Agent

class Orchestrator:

    def __init__(self):
        self.writer = Agent().get_writer()
        self.critic = Agent().get_critic()
        self.SEO_reviewer = Agent().get_SEO_reviewer()
        self.legal_reviewer = Agent().get_legal_reviewer()
        self.ethics_reviewer = Agent().get_ethics_reviewer()
        self.meta_reviewer = Agent().get_meta_reviewer()

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
    
    def generate_response(self, task:object):
        response = self.critic.initiate_chat(
            recipient=self.writer,
            message=task,
            max_turns=2,
            summary_method="last_msg"
        )
        return response
