from balsam.api import EventLog

name = 'PicoRun4.1_1E17_RHC'

# Query events for jobs in hello_multi workflow
# Every time a job changes state, an event is recorded in database
for evt in EventLog.objects.filter(tags={"workflow": f"{name}_edep_sim_rock"}):
    print("Job:", evt.job_id)  # Job ID
    print(" timestamp:", evt.timestamp)    # Time of state change (UTC)
    print(" from_state:", evt.from_state)  # State from which the job transitioned
    print(" to_state:", evt.to_state)      # State to which the job transitioned