# Downloading Prevent-AD data

When it comes to great quality data, the Prevent-AD cohort has got your back. Multi-modal imaging? Yearly visits up to four years? What more can one neuroimager ask for?

The main issue comes down to... well... actually downloading and preprocessing it. It's sheer size gives my personal computer's processor anxiety and the time it would take to process everything gives ME anxiety.

Thankfully, I was very fortunate to have access to [Beluga](https://docs.alliancecan.ca/wiki/B%C3%A9luga/en), a high performance computing resource hosted and managed by the [Digital Research Alliance of Canada (DRAC)](https://alliancecan.ca/en). Any qualified principal investigator at a Canadian institution [can apply to have access](https://alliancecan.ca/en/services/advanced-research-computing/account-management/apply-account) to computing resources. So if you are a student, you can convince your PI to apply for access!

Don't have access to a HPC? Only want a subset of participants or a specific brain modality? Or you have a dedicated local computer to do the heavy lifting for the storage and preprocessing of brain images? No sweat! The downloading process allows you a lot of flexibility for all use cases.

In the next sections, I detail how to download the data and I give an example of preprocessing said data using fMRIPrep. I also add extra precisions for when the data is downloaded to a high performance computing environment (or, well, more specific to DRAC's resources).

Note that while I try to explain things as plainly as possible, the information below does assume a certain familiarity with Python and the command line. Got questions or something isn't clear? [Open an issue on Github](https://github.com/stong3/sihnpy/issues).

## Downloading the dataset
### 1. - Navigating the Canadian Open Neuroscience Platform

The open data from the Prevent-AD cohort is made available through the [Canadian Open Neuroscience Platform portal](https://portal.conp.ca/).

```{image} ../images/conp_portal.png
:align: center
:scale: 50
```

As you'll see when you click on data there is a lot of different dataset (don't be shy... you know you want to look at all the data that are at your fingertips!). Most of them are downloaded in the same way that I will present below so feel free to use the documentation for another CONP dataset if you need.

In the search bar, if you look for "Prevent-AD", you will notice that there are three different choices:

```{image} ../images/pad_data_choice.png
:align: center
:scale: 50
```
<br>

**All three require an account to be created** but give access to different data and different data structure. Here are the differences:

| | Prevent-AD Open  | Prevent-AD Open BIDS | Prevent-AD Registered|
|------------|-----------|-----------|---------------|
| Contents   | * MRIs<br>* Basic demographics | * MRIs<br>* Basic demographics | * MRIs<br>* Detailed demographics<br>* Neuropsychology<br>* Neurosensory assessments<br>* Medical history<br>* Genetics<br>* CSF protein levels |
| Files type | `.mnc`  | `.nii`  | `.nii` |
| Structure  | All images in the<br>same directory, for<br>every participant <br>(not BIDS) | BIDS-compliant<br>structure   | BIDS-compliant structure |

The Prevent-AD Open contains the original dataset made available to researchers. It contains all available MRIs and basic demographics (ID, gender, handedness and language). Note that the images are in the MINC format (not NIFTI) and the images are not in BIDS-compliant structure. The Prevent-AD Open BIDS contains the same data, but the data is organized in BIDS and the brain scans are available in `.nii` format. Both the Prevent-AD Open and Prevent-AD Open BIDS are available to the community [by requesting an Open Access account on LORIS](https://openpreventad.loris.ca/login/request-account/) with minimal information (name, institution and institution email).

Finally, the Prevent-AD Registered contains a lot more demographic and clinical information on the participants in addition to all the MRIs available with the Prevent-AD Open and the Prevent-AD Open BIDS. However, it's access is currently restricted to faculty members from a university or physicians. If you fit that description, you can [request a Registered account on LORIS](https://registeredpreventad.loris.ca/).

```{tip}
My main recommendation would be to use the Prevent-AD Open BIDS dataset. Nowadays, a lot of software work better with BIDS-compliant structures (e.g., [fMRIPrep](https://fmriprep.org/en/stable/). Also, the images in the original Prevent-AD Open dataset comes in the [MINC (`.mnc`) format](http://bic-mni.github.io/), which work mostly with specific preprocessing tools (e.g., [CIVET](https://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Table-of-Contents)). There are tools to convert the `.mnc` format to the `.nii` format, but the data would also require BIDS formatting which can take a lot of time.
```

### 2. - Setting up Datalad

Access and download of the dataset is enabled through [Datalad](https://handbook.datalad.org/en/latest/index.html). Instructions to download the dataset are [here](https://portal.conp.ca/dataset?id=projects/preventad-open-bids). Note that instructions vary depending on what platform you are downloading the dataset.

I am not going to focus on the instructions to download Datalad which are detailed [elsewhere](https://handbook.datalad.org/en/latest/intro/installation.html), but the main idea is that you need version >=0.12.5 of DataLad and version >=8.20200309 of git-annex. Depending on your choice for installing Datalad, you might also need Python (and I mean... if you are using `sihnpy` you already have/need Python).

Once the software above is installed you can move on to the next step.

````{admonition} DRAC HPCs
:class: important
**Datalad in an high performance computer environment**

Datalad is usually very easy to install, but may require a bit more work to install on a super computer. Datalad has more extensive information on the topic [here](https://handbook.datalad.org/en/latest/intro/installation.html#linux-machines-with-no-root-access-e-g-hpc-systems). While not directly addressed on the Wiki of the Digital Research Alliance of Canada (DRAC), [others have faced issues using these resources in installing/using Datalad](https://cbs-discourse.uwo.ca/t/installing-datalad-on-compute-canada/23).

The data part of `sihnpy` has been downloaded and preprocessed directly on [Beluga](https://docs.alliancecan.ca/wiki/B%C3%A9luga/en). Throughout this section, I will give tips and tricks when using Datalad on Beluga, which should also apply on other DRAC high performance computing resources.

At the time of this writing, `git-annex` and `python/3` are modules already installed on the servers. The only step missing to install Datalad is to create a Python virtual environment in which to install it. The four lines below fully install Datalad on Beluga:

```bash
$ module load git-annex python/3        #Loads the modules
$ virtualenv ~/venv_datalad             #Creates virtual environment
$ source ~/venv_datalad/bin/activate    #Activate virtual environment
$ pip install datalad                   #Install Datalad in the virtual environment
```

Because Beluga has root privilege locked for users, installing Datalad through Python makes the most sense. Conda is also not available on the Cluster, meaning it needs to be downloaded using `pip`.

````

### 3. - Downloading the data

Now is the fun (but a bit long) part: downloading the data. From this point on, there isn't really any difference between the three Prevent-AD datasets. The steps are exactly the same and are all [detailed here](https://portal.conp.ca/dataset?id=projects/preventad-open-bids). If you are using a Python based installation of Datalad, make sure the Python environment is sourced before executing the command (this happened to me many times...)

```bash
$ datalad install https://github.com/CONP-PCNO/conp-dataset.git #Step 1 - Installs the directory structure for the CONP
$ cd conp-dataset                                               #Step 2 - Go to the directory 
$ datalad install projects/preventad-open-bids                  #Step 3 - Install specifically the Prevent-AD dataset you need
$ cd projects/preventad-open-bids/BIDS_dataset                  #Step 4 - Move to the BIDS directory you just installed (more details on this below)
```

If you now `ls` in the directory you are in, you will see the structure of the BIDS directory like so:

```bash
$ ls
dataset_description.json
participants.json
participants.tsv
README
sub-1000173
... #Etc.
```

You might think "Wow! That was so fast! Since when has my internet provider upgraded my internet to download hundreds of GBs in seconds/minutes?". 

Think again. Datalad works by downloading the directory structure of the Prevent-AD Open BIDS dataset with instructions on how to download it, but the commands above **do not actually download the data**. It's basically like if a turkey was missing its stuffing (a.k.a. the best part of turkey) but came with instructions on how to get the stuffing. If you do the following command, you should see this on your terminal:

```bash
$ ls -l
... #Etc.
participants.tsv -> ../.git/annex/objects/wV/kj/MD5E-s13031--ae9bb2da82c6ce203cffc76462810530.tsv/MD5E-s13031--ae9bb2da82c6ce203cffc76462810530.tsv
... #Etc.
```

Depending on your settings, you will likely see that the path after the arrow (../.git/annex...) will be flashing like a turn signal. Why? As I said before, Datalad doesn't download the dataset itself with `datalad install`, but the skeleton of the directory where every single file is a **soft symbolic link**. I'm not going in detail here, but just know that while the data are still soft symbolic links, there are no brain scans available to you. You need to do the last step to get it to work, which is `datalad get <filepath>`.

This part is crucial, because `datalad get` will determine what data are downloaded to your computer and how much space it will ultimately take. It is also at this stage that you should have nearby your username and password to access the Prevent-AD dataset as it will be asked from you during the process. {ref}`Remember when I mentioned to request an account above? <0.pad_data/download_pad_data:1. - Navigating the Canadian Open Neuroscience Platform>` Yeah... You won't be able to touch these cool new data until that is approved. This is usually pretty quick.

From there, you can download any and all files you want from the dataset. If you want/need to download the entire dataset, you can simply use `datalad get *`. Otherwise, you can also ask Datalad to download specific files and modalities. For instance, `datalad get sub-*/*/anat/*` will download all the anatomical scans from all participant across all timepoints. `datalad -r get sub-5555555` would download all files for participant `5555555`. You get the idea. Basically, any type of wildcard pattern that would work in Bash should also work to download the data. If you only specify a higher root directory, then you should include `-r` to ensure datalad downloads all sub-files.

````{admonition} DRAC HPCs
:class: important
**Downloading data on an HPC**

HPCs being these awesome shared resources across individuals, they also come with limitations to make it fair for all users. For example, compute nodes don't have access to the internet (at least in most HPCs of the DRAC) and memory usage is limited when on a login node. This means that the `datalad get` command needs to be slightly tweaked before it can be used properly.

First, we are forced to use a login node to download the data as we need internet access. If you were to simply do `datalad get *`, you would be met with a download that seems to stall indefinitely and potentially a crash of the node (with no helpful message to figure it out). This one bugged me for a while, until I found out that another DRAC user had a [similar issue](https://cbs-discourse.uwo.ca/t/installing-datalad-on-compute-canada/23). Basically, the trick is to force Datalad to only do one download job at a time, which doesn't eat all the memory from the login node. 

```bash
datalad get -r -J 1 sub-XXXXXX
```

Adding the `-J 1` option forces Datalad to only launch one download at a time which helps the process along. However, note that the process may take several hours to complete. For instance, downloading all anatomical data within the Prevent-AD Open BIDS took close to 8h while downloading all the functional data took close to 15h.

A good way to bypass this is to [launch a `screen` or `tmux`](https://docs.alliancecan.ca/wiki/Tmux) to launch `datalad get`, then detach from the screen. That way, even if you leave the server or your cat pours water on your computer, the download will follow along.

````
Once your files are downloaded, you will notice that if you do `ls`, you will seen a nearly identical screen as before:

```bash
$ ls -l
... #Etc.
participants.tsv -> ../.git/annex/objects/wV/kj/MD5E-s13031--ae9bb2da82c6ce203cffc76462810530.tsv/MD5E-s13031--ae9bb2da82c6ce203cffc76462810530.tsv
... #Etc.
```

However, you will see that the symbolic link is no longer flashing. This is because Datalad downloaded the file AND converted the soft symbolic link to a **hard symbolic link**. The difference regarding the type of symbolic link is not really important in this context, but just know that it allows you to copy the file to a different location without causing issues.

```{tip}
While not necessary, I do prefer to copy or move the folders Datalad collects to a different directory one `datalad get` finishes. One reason is that the path inside the `conp-dataset` directory is quite long and unnecessary. Another reason is that it simplifies the use of container apps to pre-process data.
```

And that should be it! From then you have all the data available to you. Enjoy!