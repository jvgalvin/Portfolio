# Framework for Prompt Engineering

## Context

With the rise in popularity of large language models (LLMs) like ChatGPT and GPT-4 comes advice on how best to interact with this form of artificial intelligence. My LinkedIn feed is full of posts about how to write prompts to get the desired output from ChatGPT and GPT-4. While these are likely well-intentioned and clearly topical, not a single one of them has actually been data-driven. They are purely anecdotes from a selection of users' experiences.

The purpose of this project is to provide a framework for how one can evaluate the effect of altering a prompt on the output of such models. The intention is not to provide an exhaustive list of all the ways to alter a prompt or offer context - it's purely to provide some guardrails that I think will become increasingly useful and important as usage of ChatGPT and GPT-4 rises.

## Data and Task

I'm very interested in text summarization, so I chose this as my task. I used the publicly-available SAMsum dataset, which is available for download [here](https://metatext.io/datasets/samsum).
