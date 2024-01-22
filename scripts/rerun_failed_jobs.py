from balsam.api import Job, BatchJob, Site

Job.objects.filter(state="FAILED").update(state="RESTART_READY")

# name = "PicoRun4.1_1E17_RHC"
# app_id = "spill"

# site = Site.objects.get("2x2_production")

# queue = "debug"
# project="ALCF_for_DUNE"
# job_mode="mpi"

# BatchJob.objects.create(
#     num_nodes=1,
#     wall_time_min=120,
#     queue=queue,
#     project=project,
#     site_id=site.id,
#     filter_tags={"workflow": f"{name}_{app_id}"},
#     job_mode=job_mode
# )