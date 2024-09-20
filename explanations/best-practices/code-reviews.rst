============
Code reviews
============

Writing code is a craft. There is no absolute right or wrong way of expressing thoughts into code. It's mainly contextual:

- What are the current needs?
- What are the current constraints?
- What is our current understanding of the problem?

Reviewing code is also contextual. Here below are some guidelines. They must not be applied in every circumstance. Instead, they define a baseline in terms of expectations on the team.

Requesting a review
===================

- **Load:** requests should be well balanced among team members so we don't overload a single individual.
- **Cognitive load:** it's easier for the human brain to focus on several things, one by one, rather than one big thing. Split your changes into several atomic commits. That will speed up the review.
- **Context:** provide information about why you are proposing this change. It can either be the commit message, the Pull Request title, or the bug report itself.
- **Evidence:** provide evidence to support any assertions made in your commit message. Eg: "this feature/table/worker is unused" should include pointers to some due diligence that you have done to verify that.
- **All green:** ensure required checks are passing before submitting review request by creating

  - the Pull Request as Draft
  - or the Phabricator revision as "Changes planned".

- **Reminders:** if you don't get any feedback within 2 business days, do not hesitate to ping the reviewer.

Performing a review
===================

- **Timing:** Reviewers should endeavour to reply within one business day of the request, and are expected to reply within 2. If not, the reviewer should reach out to the author to extend the expected relay or redirect to another reviewer.
- **Tone:** remain considerate. We all make mistakes and we can all learn from each other.
- **Context:** feel free to ask more information from the author. Use "Request Changes" to put the review back in the author's queue.
- **Posterity:** when a conversation happens on a private or temporary medium, put information back in the review.
- **Knowledge:** do not feel obligated to review if you don’t have enough experience/context.
- **Trust, but verify:** verify any non-obvious assertions made in the review request, or implied in changes to the code. Everyone makes mistakes, and an important part of reviewing is catch them before the cause issues!
- **Pass:** if you know who the best person for review is, remove yourself/the review group and tag the right person directly
- **Focus:** no need to review what CI already checks (linters, unchanged tests). New/changed tests must be read to ensure they check what the author intends.
- **Changes needed:** you are empowered to push back when something important is missing (test coverage, lack of context, important cases not covered).
- **Follow-up:** if the patch is urgent, you can explicitly request a follow-up patch to fill the holes.
