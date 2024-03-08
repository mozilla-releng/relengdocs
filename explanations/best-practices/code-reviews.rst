============
Code reviews
============

Writing code is a craft. There is no absolute right or wrong way of expressing thoughts into code. It's mainly contextual:

* What the current needs?
* What are the current constraints?
* What is our current understanding of the problem?

Reviewing code is also contextual. Here below are some guidelines. They must not be applied in every circumstance. Instead, they define a baseline in terms of expectations on the team.

Requesting a review
===================

* **Timing:** expect the reviewer to come back after a day or two, in order to take timezones into account.
* **Load:** requests should be well balanced among team members so we don't overload a single individual.
* **Reminders:** the Slack channel `#releng-notifications <https://app.slack.com/client/T027LFU12/CN77C0BUG>`__ will remind the reviewer when there is an outstanding request.
* **Cognitive load:** it's easier for the human brain to focus on several things, one by one, rather than one big thing. Split your review into several atomic commits. That will speed up the review.
* **Context:** provide information about why you are proposing this change.
  * when the bug report is straightforward, in the commit message and the Pull Request title
  * when the bug report is require lots of back-and-forth between people, on the bug report itself.
* **All green:** ensure required checks must be passing before submitting review request


Performing a review
===================

* **Tone:** remain considerate. We all make mistakes and we can all learn from each other.
* **Context:** feel free to ask more information from the author.
* **Posterity:** when a conversation happens on a private or temporary medium, put information back in the review.
* **Knowledge:** do not feel obligated to review if you don’t have enough experience/context.
* **Pass:** if you know who the best person for review is, remove yourself/the review group and tag the right person directly
* **Focus:** no need to review what CI already checks (linters, passing tests)
* **Changes needed:** you are empowered to push back when something important is missing (test coverage, lack of context, important cases not covered).
* **Follow-up:** if the patch is urgent, you can explicitly request a follow-up patch to fill the holes.
