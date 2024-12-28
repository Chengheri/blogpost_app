import autogen

class Agent:
    
    def __init__(self, llm_config:dict):
        self.llm_config = llm_config

    def get_writer(self):
        writer = autogen.AssistantAgent(
            name="Writer",
            system_message="You are a writer. You write engaging and concise " 
                "blogpost (with title) on given topics. You must polish your "
                "writing based on the feedback you receive and give a refined "
                "version. Only return your final work without additional comments.",
            llm_config=self.llm_config,
        )
        return writer

    def get_critic(self):
        critic = autogen.AssistantAgent(
            name="Critic",
            is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
            llm_config=self.llm_config,
            system_message="You are a critic. You review the work of "
                        "the writer and provide constructive "
                        "feedback to help improve the quality of the content.",
        )
        return critic

    def get_SEO_reviewer(self):
        SEO_reviewer = autogen.AssistantAgent(
            name="SEO Reviewer",
            llm_config=self.llm_config,
            system_message="You are an SEO reviewer, known for "
                "your ability to optimize content for search engines, "
                "ensuring that it ranks well and attracts organic traffic. " 
                "Make sure your suggestion is concise (within 3 bullet points), "
                "concrete and to the point. "
                "Begin the review by stating your role.",
        )
        return SEO_reviewer

    def get_legal_reviewer(self):
        legal_reviewer = autogen.AssistantAgent(
            name="Legal Reviewer",
            llm_config=self.llm_config,
            system_message="You are a legal reviewer, known for "
                "your ability to ensure that content is legally compliant "
                "and free from any potential legal issues. "
                "Make sure your suggestion is concise (within 3 bullet points), "
                "concrete and to the point. "
                "Begin the review by stating your role.",
        )
        return legal_reviewer

    def get_ethics_reviewer(self):
        ethics_reviewer = autogen.AssistantAgent(
            name="Ethics Reviewer",
            llm_config=self.llm_config,
            system_message="You are an ethics reviewer, known for "
                "your ability to ensure that content is ethically sound "
                "and free from any potential ethical issues. " 
                "Make sure your suggestion is concise (within 3 bullet points), "
                "concrete and to the point. "
                "Begin the review by stating your role. ",
        )
        return ethics_reviewer

    def get_meta_reviewer(self):
        meta_reviewer = autogen.AssistantAgent(
            name="Meta Reviewer",
            llm_config=self.llm_config,
            system_message="You are a meta reviewer, you aggragate and review "
            "the work of other reviewers and give a final suggestion on the content.",
        )
        return meta_reviewer

