==============================
Handoffs and Incident Response
==============================

When we need to respond to some sort of incident (some bustage, a release request, etc.), sometimes these tasks are larger than a single person can handle, or require enough time and urgency that they cannot be completed during a single person's working hours.

These are best practices for handoffs and incident response. As of 2022.01.12 we haven't exercised this muscle much, so we may fall short of these ideals, but we should aspire to reach them.

Incident doc or bug
===================

The history of a given incident can easily span multiple channels, bugs, docs, zoom calls, etc., and recreating the timeline, outstanding issues or questions, or other status can be difficult.

It's best practice to have a single document or bug where important events, patches, other documents can be recorded or linked.

We can formalize this with checklists and other templates if and when we build this muscle, but at first, just having that single source of truth document or bug is good.

Handoffs
========

Clear and explicit communication is key. Over-communication is preferable to under-communication.

(And how we respond is important too. To paraphrase :joduinn, when the s*** hits the fan and everyone's scrambling trying to figure out what's going on and how to get it resolved, Releng will be calm, prepared, and ready to handle the crisis.

Certainly something to aspire to :)

Explicit wording and handoffs between teams
-------------------------------------------

Sometimes the baton needs to be passed between teams: the build goes to QA, QA signs off, Relman says "go", Releng pushes it somewhere. And often with Releng, un-shipping a release is more difficult and messy than holding off on the release until we have all of our concerns addressed.

In these cases, explicit wording is important. "It seems better" as a response in channel, where it's not clear which question is being responded to, where "it" is vague, "better" is relative but not precise, and "seems" adds a qualifier to the entire statement. "QA signs off on Firefox 96.0.1". "Releng has no more concerns about the readiness of ESR 91.5.1". "Please ship Focus 97.0 to users".

A single incident commander
---------------------------

A single incident commander is best. Crowd-sourcing can be effective for gathering status, but ideally one person makes decisions to avoid confusion, miscommunication, and decisions made without full context.

For instance, if Alice says "Please hold the release of Product 2.0.3 because of ____ concerns," then disappears to track those down. If Bob believes he has full context but doesn't, and he says "Yeah, we can proceed" without explicitly checking with Alice, we may be shipping a build with unaddressed issues.

In the above example, if there were a single Incident Commander, Alice would express her concerns to that IC, and either the IC would hold off until every item were addressed, or check with Alice before proceeding.

In the case where the IC has reached the end of their day, ideally they explicitly hand off to another IC (see below).

Handoffs between team members
-----------------------------

Especially when ending your day and handing off to another team member, it's important to:

1. Find another owner to hand off to, ideally in the next timezone: "I'm ending my day in 1hr. Beatrice, are you available to take the Incident_Name handoff?"

2. Be explicit about current status (what you've done, what still needs to be done): "The checklist in bug 123456 is up to date. I will try to finish step 4 by my EOD (and will update you). Can you pick up with step 5 in an hour? Relman wants us to ping them when we're done." Sometimes they will have questions about what is needed for next steps, and this overlap will allow for clarification. (If you need to do an async handoff due to lack of timezone overlap, writing everything down clearly becomes even more important.)

This avoids the next person wasting time trying to verify what you have or haven't done, avoids duplication of effort, and avoids missing critical steps.

Timely Retrospectives
=====================

Ok, something's gone south and we've had to respond at emergency priority levels. Once we've gotten some sleep but while it's still fresh in our minds, let's write down timelines, what happened, who did what, root causes, what went well, what could have gone better, etc. Then let's plan for ways to make the next time at least incrementally better.
