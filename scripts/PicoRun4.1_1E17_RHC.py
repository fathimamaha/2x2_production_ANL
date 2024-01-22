from balsam.api import ApplicationDefinition, BatchJob, Job, Site
import yaml

#Machine variables
#########################
queue = "debug"         #
project="ALCF_for_DUNE" #
job_mode="mpi"          #
#########################

name = 'PicoRun4.1_1E17_RHC'
yaml_dir = f'../specs/{name}/{name}'
start = 0
single_size = 100
spill_size = 10 

# runs = ["all","mid_submit"]
# runs = ["submit_all"]
# runs = ["larnd","submit_all"]
# runs = ["flow","submit_all"]
runs = ["plot","submit_all"]
# runs = ["edepsim_nu"]
# runs = ["edepsim_nu"]
# runs = ["hadd_nu","hadd_rock","submit_all"]
# runs = ["spill","submit_all"]
# runs = ["convert2h5","submit_all"]
# runs = ["larnd","submit_all"]

version = "v4"

"""
Functions
"""

def get_env_from_yaml(extension, idx):
    yaml_file_path = f'{yaml_dir}{extension}'
    with open(yaml_file_path, 'r') as file:
        yaml_content = file.read()
    yaml_dict = yaml.safe_load(yaml_content)
    env = yaml_dict['base_envs'][idx]['env']
    return env

def create_jobs(app_id, size, node_packing_count):

    for i in range(size):
        Job.objects.create( app_id=app_id,
                            site_name="2x2_production",
                            workdir=f"workdir/{i}_{app_id}",
                            node_packing_count=node_packing_count,
                            tags={"workflow": f"{name}_{app_id}_{version}"},
                            data={"i": i})

def create_single_dependent_job(app_id, i, parent_ids, node_packing_count):

    Job.objects.create( app_id=app_id,
                        site_name="2x2_production",
                        workdir=f"workdir/{i}_{app_id}",
                        node_packing_count=node_packing_count,
                        tags={"workflow": f"{name}_{app_id}_{version}"},
                        data={"i": i},
                        parent_ids=parent_ids)

def submit_filtered_jobs(app_id, num_nodes=1, wall_time_min = 60):

    site = Site.objects.get("2x2_production")

    BatchJob.objects.create(
        num_nodes=num_nodes,
        wall_time_min=wall_time_min,
        queue=queue,
        project=project,
        site_id=site.id,
        filter_tags={"workflow": f"{name}_{app_id}_{version}"},
        job_mode=job_mode
    )

def submit_all_jobs(num_nodes=1, wall_time_min = 60):

    site = Site.objects.get("2x2_production")

    BatchJob.objects.create(
        num_nodes=num_nodes,
        wall_time_min=wall_time_min,
        queue=queue,
        project=project,
        site_id=site.id,
        job_mode=job_mode
    )

"""
nu - edepsim
------------------------------------------
"""

extension = ".nu.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "edep_sim_nu"

class edep_sim_nu(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_edep_sim.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-edep-sim
        '''

edep_sim_nu.sync()

if "edepsim_nu" in runs or "all" in runs:
    create_jobs(app_id, single_size, single_size)
    submit_filtered_jobs(app_id)

"""
nu-edepsim batchjobs created and submitted
------------------------------------------
"""

"""
rock-edepsim
------------------------------------------
"""

extension = ".rock.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "edep_sim_rock"

class edep_sim_rock(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_edep_sim.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-edep-sim
        '''

edep_sim_rock.sync()

if "edepsim_rock" in runs or "all" in runs:
    create_jobs(app_id, single_size, single_size)
    submit_filtered_jobs(app_id)

"""
rock-edepsim batchjobs created and submitted
------------------------------------------
"""

"""
nu-hadd
------------------------------------------
"""


extension = ".hadd.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "hadd_nu"

class hadd_nu(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_hadd.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-hadd
        '''

hadd_nu.sync()

if "hadd_nu" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_edep_sim_nu_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)
    
    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)


"""
------------------------------------------
"""


"""
rock-hadd
------------------------------------------
"""

extension = ".hadd.yaml"
env = get_env_from_yaml(extension, 1)
app_id = "hadd_rock"

class hadd_rock(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_hadd.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-hadd
        '''

hadd_rock.sync()

if "hadd_rock" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_edep_sim_rock_{version}"}
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)
    
    # submit_filtered_jobs(app_id)
if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

"""
------------------------------------------
"""

"""
spill-build
------------------------------------------
"""
# scripts/fwsub.py --runner SimFor2x2_v3_LArND --base-env "$name".larnd --name "$name".larnd --size $spill_size --start $start
# scripts/fwsub.py --runner SimFor2x2_v3_Flow --base-env "$name".flow --size $spill_size --start $start
# scripts/fwsub.py --runner SimFor2x2_v3_Plots --base-env "$name".plots --size $spill_size --start $start

extension = ".spill.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "spill"

class spill(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_spill_build.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-spill-build
        '''

spill.sync()

if "spill" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_hadd_nu_{version}"},
        )]+[job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_hadd_rock_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)
if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

"""
------------------------------------------
"""

"""
convert2h5
------------------------------------------
"""


extension = ".convert2h5.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "convert2h5"

class convert2h5(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_convert2h5.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-convert2h5
        '''

convert2h5.sync()

if "convert2h5" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_spill_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)
"""
------------------------------------------
"""

"""
larnd
------------------------------------------
"""


extension = ".larnd.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "larnd"

class larnd(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_larnd_sim.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-larnd-sim
        '''

larnd.sync()

if "larnd" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_convert2h5_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, 1)

    # submit_filtered_jobs(app_id)
if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

"""
------------------------------------------
"""


"""
flow
------------------------------------------
"""


extension = ".flow.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "flow"

class flow(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_ndlar_flow.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/run-ndlar-flow
        '''

flow.sync()

if "flow" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_larnd_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)
"""
------------------------------------------
"""


"""
plot
------------------------------------------
"""


extension = ".plot.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "plot"

class plot(ApplicationDefinition):
    site = "2x2_production"
    print(env)
    environment_variables = env
    
    command_template = "./run_validation.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd /home/fathimamaha/2x2_production/data/2x2_sim/validation
        '''

plot.sync()

if "plot" in runs or "all" in runs:

    site = Site.objects.get("2x2_production")

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_convert2h5_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "submit_all" in runs:
    submit_all_jobs()





