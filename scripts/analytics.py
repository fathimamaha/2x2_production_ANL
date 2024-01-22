from balsam.api import models, BatchJob
from balsam.api import EventLog,Job
from balsam.analytics import throughput_report
from balsam.analytics import utilization_report
from matplotlib import pyplot as plt
from balsam.analytics import available_nodes

# name = 'PicoRun4.1_1E17_RHC'
# app_id = "edep_sim_rock"

# # Fetch jobs and events for the Hello app
# app = models.App.objects.get(site_name="2x2_production",name=app_id)
# jl = Job.objects.filter(app_id=app.id,tags={"workflow":f"{name}_{app_id}_v4"})

# events = EventLog.objects.filter(job_id=[job.id for job in jl])

# # Generate a throughput report
# times, done_counts = throughput_report(events, to_state="JOB_FINISHED")

# t0 = min(times)
# elapsed_minutes = [(t - t0).total_seconds() / 60 for t in times]
# plt.step(elapsed_minutes, done_counts, where="post")

# # Generate a utilization report
# times, util = utilization_report(events, node_weighting=True)

# t0 = min(times)
# elapsed_minutes = [(t - t0).total_seconds() / 60 for t in times]
# plt.step(elapsed_minutes, util, where="post")


# foo_batchjobs = BatchJob.objects.filter(
#     filter_tags={"workflow":f"{name}_{app_id}_v4"}
# )
# times, node_counts = available_nodes(foo_batchjobs)
# t0 = min(times)
# elapsed_minutes = [(t - t0).total_seconds() / 60 for t in times]
# # plt.plot(elapsed_minutes, node_counts, where="post")
# plt.savefig(f"summary_{name}_{app_id}.png")





name = 'PicoRun4.1_1E17_RHC'
app_id = "edep_sim_nu"

# Fetch jobs and events for the Hello app
app = models.App.objects.get(site_name="2x2_production", name=app_id)
jl = Job.objects.filter(app_id=app.id, tags={"workflow": f"{name}_{app_id}_v4"}, state="JOB_FINISHED")

events = EventLog.objects.filter(job_id=[job.id for job in jl])
print(events)
# Generate a utilization report
times, util = utilization_report(events, node_weighting=True)

# Plot utilization
t0 = min(times)
elapsed_minutes1 = [(t - t0).total_seconds() / 60 for t in times]

# print(util)

# Generate node count report
foo_batchjobs = BatchJob.objects.filter(filter_tags={"workflow": f"{name}_{app_id}_v4"})
times, node_counts = available_nodes(foo_batchjobs)
t0 = min(times)
elapsed_minutes = [(t - t0).total_seconds() / 60 for t in times]
# Plot node count with thick grey translucent lines
plt.plot(elapsed_minutes, node_counts, color='grey', linewidth=2, alpha=0.5, label='Node Count')
util_fraction = [u * max(node_counts) for u in util]  # Scale utilization between 0 to 1
plt.step(elapsed_minutes1, util_fraction, where="post", label='Utilization')


# Set labels and legend
plt.xlabel('Elapsed Time (minutes)')
plt.ylabel('Utilization / Node Count')
plt.legend()

# Save the plot
plt.savefig(f"summary_{name}_{app_id}.png")







# from balsam.api import BatchJob
# from balsam.analytics import available_nodes

# foo_batchjobs = BatchJob.objects.filter(
#     filter_tags={"workflow":f"{name}_{app_id}"}
# )
# times, node_counts = available_nodes(foo_batchjobs)
# from balsam.api import BatchJob
# from balsam.analytics import available_nodes

# foo_batchjobs = BatchJob.objects.filter(
#     filter_tags={"workflow":f"{name}_{app_id}"}
# )

# # node count
# plt.figure()
# times, node_counts = available_nodes(foo_batchjobs)
# # print(node_counts)
# # t0 = min(times)
# elapsed_minutes = [(t - t0).total_seconds() / 60 for t in times]
# plt.step(elapsed_minutes, node_counts, where="post")
# plt.xlabel("Elapsed time (minutes)")
# plt.ylabel("Node Count")
# plt.savefig("node_count.png")




####

# from balsam.api import EventLog, BatchJob
# from balsam.analytics import throughput_report, utilization_report, available_nodes
# from matplotlib import pyplot as plt

# # Filter EventLog and BatchJob based on your requirements
# # events = EventLog.objects.filter(scheduler_id=123)
# foo_batchjobs = BatchJob.objects.filter(filter_tags={"workflow":f"{name}_{app_id}_v4"})

# app = models.App.objects.get(site_name="2x2_production",name=app_id)
# jl = Job.objects.filter(app_id=app.id,tags={"workflow":f"{name}_{app_id}_v4"})
# events = EventLog.objects.filter(job_id=[job.id for job in jl])

# # Throughput report
# times, done_counts = throughput_report(events, to_state="JOB_FINISHED")
# t0 = min(times)
# elapsed_minutes = [(t - t0).total_seconds() / 60 for t in times]

# # Utilization report
# times, util = utilization_report(events, node_weighting=True)
# t0 = min(times)
# elapsed_minutes_util = [(t - t0).total_seconds() / 60 for t in times]

# # Available Nodes
# times_nodes, node_counts = available_nodes(foo_batchjobs)

# # Plotting
# fig, ax1 = plt.subplots()

# # Throughput plot
# ax1.step(elapsed_minutes, done_counts, where="post", label="Throughput", color='blue')
# ax1.set_xlabel('Elapsed Minutes')
# ax1.set_ylabel('Throughput', color='blue')
# ax1.tick_params('y', colors='blue')

# # Utilization plot
# ax2 = ax1.twinx()
# ax2.step(elapsed_minutes_util, util, where="post", label="Utilization", color='green')
# ax2.set_ylabel('Utilization', color='green')
# ax2.tick_params('y', colors='green')

# # Available Nodes plot
# ax3 = ax1.twinx()
# ax3.step(times_nodes, node_counts, where="post", label="Available Nodes", color='gray')
# ax3.set_ylabel('Available Nodes', color='gray')
# ax3.spines['right'].set_position(('outward', 60))  # adjust the position of the right axis
# ax3.tick_params('y', colors='gray')

# fig.tight_layout()
# plt.title("Job Throughput, Utilization, and Available Nodes")
# plt.savefig("analytics.png")
