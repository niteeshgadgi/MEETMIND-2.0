DEMO_TRANSCRIPTS = {
    "week_1": {
        "name": "Week 1 — Q3 Sprint Kickoff",
        "transcript": """Maya: Alright, let's get started. We need to lock in the tech stack and timeline today.
Rohan: I've been evaluating options. I think React for frontend and FastAPI for the backend is our best bet. Both have strong ecosystems and I'm most productive with them.
Maya: Agreed, let's go with that. Decision made — React plus FastAPI. Rohan, you're owning the infrastructure setup?
Rohan: Yes, I'll have the base infrastructure ready by Friday. That includes CI/CD, environment configs, and the database setup.
Priya: I'll have the wireframes done by next Wednesday. I've already started on the dashboard home screen.
Maya: Good. On pricing — I've been doing competitive research. $29 per user per month puts us right between Notion and Loom. I think it's justified given the AI features.
Rohan: Works for me. Keeps us competitive without underselling.
Maya: Decision: $29/month per user. Launch target is 8 weeks from today.
Priya: Which analytics provider are we going with? I need to know for the instrumentation layer in the designs.
Rohan: I've been going back and forth on Mixpanel versus Amplitude. Mixpanel is cheaper but Amplitude has better cohort analysis. I haven't decided yet.
Maya: That's an open question then. Can you have a recommendation by Thursday?
Rohan: Yes, I'll compare them properly and send a Slack summary.
Maya: Last thing — legal still hasn't approved the data processing agreement. We cannot go live without that. Sam, can you follow up with them today?
Rohan: That's a real blocker. Everything else can ship but that DPA is on the critical path.
Maya: Agreed. Rohan sets up infrastructure by Friday, Priya delivers wireframes by Wednesday, and legal DPA follow-up is on Maya."""
    },
    "week_2": {
        "name": "Week 2 — Infrastructure Review",
        "transcript": """Maya: Welcome Sam, glad you're joining us from today.
Sam: Thanks, excited to be here. I've been catching up on the docs.
Rohan: Infrastructure is done. CI/CD is live, staging environment is up, database is provisioned. One issue though — I ran into Mixpanel's API rate limits during integration testing. At our projected event volume we'd hit the cap within 2 hours of a busy day.
Maya: That's a serious problem. What's the alternative?
Rohan: Amplitude doesn't have those same limits at our tier. I recommend we switch.
Maya: Decision: we're going with Amplitude. Sam, can you get on a call with their sales team and negotiate pricing?
Sam: On it. I'll reach out today and try to close something by end of week.
Priya: Wireframes are done. I want to walk through three screen designs — dashboard home, the event timeline view, and the integration settings panel. The team approved the dashboard home last week so let's focus on the other two.
Maya: Let's look at the timeline view first.
Priya: The idea is a scrollable feed with filters on the left. Clean, no clutter. Team liked it, no major changes.
Maya: Good. Settings panel?
Priya: Standard form layout. Rohan flagged that the webhook configuration section needs to connect to the backend — that's a dependency we need to plan for.
Rohan: I can build that out in week 3.
Maya: The legal DPA is still not signed. I sent a follow-up yesterday. Their legal team is backed up apparently. This is now officially on the critical path — it blocks our public launch.
Sam: Is there any way to do a soft launch or private beta while we wait?
Maya: Good question — let's revisit that next week.
Rohan: Integrate Amplitude by Thursday. Sam closes the Amplitude deal. Legal DPA still pending."""
    },
    "week_3": {
        "name": "Week 3 — Beta Launch Planning",
        "transcript": """Sam: Good news — Amplitude deal is closed. $800 per month, 2 million events included. We negotiated a 20% discount from their list price.
Maya: Excellent. That's within budget. 
Rohan: Integration is at 70%. I've hit a snag with the webhook handling — specifically around retry logic when the receiving endpoint is down. I need help thinking through the failure states.
Maya: Can you pair with Priya on that or does this need a backend specialist?
Rohan: It's mostly backend. I'll document the edge cases and we can revisit Thursday.
Maya: Legal DPA update — I sent them the final version yesterday. They confirmed they received it and their team is reviewing. Estimate is 3 to 5 business days for signature.
Sam: So we could have it signed by end of next week?
Maya: Possibly. Which brings me to the question from last week — soft launch. I say we launch to beta users without any marketing while we wait for legal to finish.
Priya: I support that. We have 12 companies on the waitlist who explicitly said they're okay with beta terms.
Sam: I can draft the beta agreement language today so we're covered legally on that front.
Maya: Decision: soft launch with beta users only, no marketing, while legal finalizes the DPA. Priya, you're owning the onboarding email sequence for those 12 companies.
Priya: I'll have drafts ready by Wednesday. One thing — the mobile responsive version wasn't in the original scope. I've had three beta companies ask for it specifically. Adding it properly is about 3 extra days of design work.
Maya: Let's add it. We can absorb 3 days. Adjust the timeline accordingly.
Rohan: That puts integration completion at next Monday instead of this Friday.
Maya: Acceptable. Priya owns beta onboarding emails by Wednesday, Rohan completes Amplitude integration by Monday, Sam drafts beta agreement today."""
    }
}

DEMO_WORKSPACE = "demo-team-alpha"
