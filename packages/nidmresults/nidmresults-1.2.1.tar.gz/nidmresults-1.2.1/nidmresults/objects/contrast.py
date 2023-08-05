"""
Objects describing the Contrast Estimation activity, its inputs and outputs as
specified in NIDM-Results.

Specification: http://nidm.nidash.org/specs/nidm-results.html

@author: Camille Maumet <c.m.j.maumet@warwick.ac.uk>
@copyright: University of Warwick 2013-2014
"""
import numpy as np
import os
from nidmresults.objects.constants import *
import nibabel as nib
from nidmresults.objects.generic import *
import uuid


class Contrast(object):

    """
    Object representing a Contrast Estimation step: including a
    ContrastEstimation activity, its inputs and outputs.
    """

    def __init__(self, contrast_num, contrast_name, weights, estimation,
                 contrast_map, stderr_or_expl_mean_sq_map, stat_map,
                 z_stat_map=None):
        super(Contrast, self).__init__()
        # FIXME: contrast_num migth only be defined in FSL if this is not
        # generic the class should be overloaded in fsl_objects
        self.contrast_num = contrast_num
        self.contrast_name = contrast_name
        self.weights = weights
        self.estimation = estimation
        self.contrast_map = contrast_map
        self.stderr_or_expl_mean_sq_map = stderr_or_expl_mean_sq_map
        self.stat_map = stat_map
        self.z_stat_map = z_stat_map


class ContrastWeights(NIDMObject):

    """
    Object representing a ContrastWeight entity.
    """

    def __init__(self, contrast_num, contrast_name, contrast_weights,
                 stat_type):
        super(ContrastWeights, self).__init__()
        self.contrast_name = contrast_name
        self.contrast_weights = contrast_weights
        self.contrast_num = contrast_num
        self.stat_type = stat_type
        self.id = NIIRI[str(uuid.uuid4())]
        self.type = STATO_CONTRAST_WEIGHT_MATRIX
        self.prov_type = PROV['Entity']

    def export(self, nidm_version):
        """
        Create prov graph.
        """
        label = "Contrast Weights: " + self.contrast_name

        if self.stat_type.lower() == "t":
            stat = STATO_TSTATISTIC
        elif self.stat_type.lower() == "z":
            stat = STATO_ZSTATISTIC
        elif self.stat_type.lower() == "f":
            stat = STATO_FSTATISTIC

        self.add_attributes((
            (PROV['type'], STATO_CONTRAST_WEIGHT_MATRIX),
            (NIDM_STATISTIC_TYPE, stat),
            (PROV['label'], label),
            (NIDM_CONTRAST_NAME, self.contrast_name),
            (PROV['value'], self.contrast_weights)))


class ContrastMap(NIDMObject):

    """
    Object representing a ContrastMap entity.
    """

    def __init__(self, contrast_file, contrast_num, contrast_name,
                 coord_space, export_dir, ident=None):
        super(ContrastMap, self).__init__(export_dir)
        self.num = contrast_num
        self.name = contrast_name
        if ident is None:
            self.id = NIIRI[str(uuid.uuid4())]
        else:
            self.id = ident
        filename = 'Contrast' + self.num + '.nii.gz'
        self.file = NIDMFile(self.id, contrast_file, filename, export_dir)
        self.coord_space = coord_space
        self.type = NIDM_CONTRAST_MAP
        self.prov_type = PROV['Entity']
        self.label = "Contrast Map: " + self.name

    def export(self, nidm_version):
        """
        Create prov graph.
        """
        # Contrast Map entity
        self.add_attributes((
            (PROV['type'], NIDM_CONTRAST_MAP),
            (NIDM_IN_COORDINATE_SPACE, self.coord_space.id),
            (NIDM_CONTRAST_NAME, self.name),
            (PROV['label'], self.label)))


class ContrastExplainedMeanSquareMap(NIDMObject):
    """
    Object representing a ContrastExplainedMeanSquareMap entity.
    """
    def __init__(self, stat_file, sigma_sq_file, contrast_num,
                 coord_space, export_dir):
        super(ContrastExplainedMeanSquareMap, self).__init__(export_dir)
        self.stat_file = stat_file
        self.sigma_sq_file = sigma_sq_file
        self.num = contrast_num
        self.id = NIIRI[str(uuid.uuid4())]
        self.coord_space = coord_space
        self.type = NIDM_CONTRAST_EXPLAINED_MEAN_SQUARE_MAP
        self.prov_type = PROV['Entity']

    def export(self, nidm_version):
        """
        Create prov graph.
        """
        # Create Contrast Explained Mean Square Map as fstat<num>.nii.gz
        # multiplied by sigmasquareds.nii.gz and save it in export_dir
        fstat_img = nib.load(self.stat_file)
        fstat = fstat_img.get_data()

        sigma_sq_img = nib.load(self.sigma_sq_file)
        sigma_sq = sigma_sq_img.get_data()

        expl_mean_sq = nib.Nifti1Image(fstat*sigma_sq, fstat_img.get_qform())

        expl_mean_sq_filename = \
            "ContrastExplainedMeanSquareMap" + self.num + ".nii.gz"
        expl_mean_sq_file = os.path.join(
            self.export_dir, expl_mean_sq_filename)
        nib.save(expl_mean_sq, expl_mean_sq_file)

        self.file = NIDMFile(self.id, expl_mean_sq_file,
                             expl_mean_sq_filename, self.export_dir)

        # Contrast Explained Mean Square Map entity
        path, filename = os.path.split(expl_mean_sq_file)
        self.add_attributes((
            (PROV['type'], self.type),
            (NIDM_IN_COORDINATE_SPACE, self.coord_space.id),
            (PROV['label'], "Contrast Explained Mean Square Map")))


class ContrastStdErrMap(NIDMObject):

    """
    Object representing a ContrastStdErrMap entity.
    """

    def __init__(self, contrast_num, filepath, is_variance, coord_space,
                 var_coord_space, export_dir):
        super(ContrastStdErrMap, self).__init__(export_dir)
        self.file = filepath
        self.id = NIIRI[str(uuid.uuid4())]
        self.is_variance = is_variance
        self.num = contrast_num
        self.coord_space = coord_space
        if is_variance:
            self.var_coord_space = var_coord_space
        self.type = NIDM_CONTRAST_STANDARD_ERROR_MAP
        self.prov_type = PROV['Entity']

    def export(self, nidm_version):
        """
        Create prov graph.
        """
        filename = "ContrastStandardError" + self.num + ".nii.gz"
        if self.is_variance:
            # Copy contrast variance map in export directory
            path, var_cope_filename = os.path.split(self.file)
            contrast_var = ContrastVariance(
                self.var_coord_space, self.file, var_cope_filename)
            self.contrast_var = contrast_var

            # Create standard error map from contrast variance map
            var_cope_img = nib.load(self.file)
            contrast_variance = var_cope_img.get_data()

            standard_error_img = nib.Nifti1Image(np.sqrt(contrast_variance),
                                                 var_cope_img.get_qform())

            stderr_file = os.path.join(self.export_dir, filename)
            nib.save(standard_error_img, stderr_file)
            self.file = NIDMFile(
                self.id, stderr_file, filename, self.export_dir)

        else:
            self.file = NIDMFile(self.id, self.file, None, self.export_dir)

        self.add_attributes((
            (PROV['type'], self.type),
            (DCT['format'], "image/nifti"),
            (NIDM_IN_COORDINATE_SPACE, self.coord_space.id),
            (PROV['label'], "Contrast Standard Error Map")))


class ContrastVariance(NIDMObject):
    def __init__(self, coord_space, var_file, filename):
        super(ContrastVariance, self).__init__()
        self.id = NIIRI[str(uuid.uuid4())]
        self.coord_space = coord_space
        self.type = NIDM_CONTRAST_VARIANCE_MAP
        self.file = NIDMFile(self.id, var_file)
        self.filename = filename
        self.prov_type = PROV['Entity']

    def export(self, nidm_version):
        self.add_attributes([(PROV['type'], NIDM_CONTRAST_VARIANCE_MAP)])


class StatisticMap(NIDMObject):

    """
    Object representing a StatisticMap entity.
    """

    def __init__(self, location, stat_type, contrast_name, dof, coord_space,
                 contrast_num=None, export_dir=None, label=None, oid=None,
                 format="image/nifti", effdof=None, filename=None, sha=None,
                 contrast_estimation=None):
        super(StatisticMap, self).__init__(export_dir, oid=oid)
        self.num = contrast_num
        self.contrast_name = contrast_name
        self.stat_type = stat_type
        if self.stat_type.lower() == "t":
            self.stat = STATO_TSTATISTIC
        elif self.stat_type.lower() == "z":
            self.stat = STATO_ZSTATISTIC
        elif self.stat_type.lower() == "f":
            self.stat = STATO_FSTATISTIC
        # FIXME use new 'preferred mathematical notation from stato'
        if self.num is not None:
            filename = self.stat_type.upper() + \
                'Statistic' + self.num + '.nii.gz'
        self.file = NIDMFile(self.id, location, filename, export_dir, sha=sha)
        self.coord_space = coord_space
        self.dof = dof
        self.type = NIDM_STATISTIC_MAP
        self.prov_type = PROV['Entity']
        if label is not None:
            self.label = label
        else:
            self.label = "Statistic Map: " + self.contrast_name
            # Include statistic type in the label
            self.label = self.stat_type + '-' + self.label

        self.format = format
        if effdof is None:
            # FIXME: this should not be 1 for F-test
            effdof = 1.0

        self.effdof = effdof

        # Only used when reading (so far)
        self.contrast_estimation = contrast_estimation

    def __str__(self):
        return '%s\t%s' % (self.label, self.file)

    def export(self, nidm_version):
        """
        Create prov graph.
        """
        attributes = [(PROV['type'], NIDM_STATISTIC_MAP),
                      (DCT['format'], self.format),
                      (PROV['label'], self.label),
                      (NIDM_STATISTIC_TYPE, self.stat),
                      (NIDM_CONTRAST_NAME, self.contrast_name),
                      (NIDM_IN_COORDINATE_SPACE, self.coord_space.id)]

        if not self.stat_type == 'Z':
            attributes.insert(0, (NIDM_ERROR_DEGREES_OF_FREEDOM, self.dof))
            attributes.insert(0, (NIDM_EFFECT_DEGREES_OF_FREEDOM, self.effdof))
        else:
            # For Z-Statistic error dof is infinity and effect dof is 1
            attributes.insert(0, (NIDM_ERROR_DEGREES_OF_FREEDOM, float("inf")))
            attributes.insert(0, (NIDM_EFFECT_DEGREES_OF_FREEDOM, self.effdof))

        # Create "Statistic Map" entity
        # FIXME: Deal with other than t-contrast maps: dof + statisticType
        self.add_attributes(attributes)


class ContrastEstimation(NIDMObject):

    """
    Object representing a ContrastEstimation entity.
    """

    def __init__(self, contrast_num, contrast_name=None, label=None,
                 param_estimate=None, oid=None):
        super(ContrastEstimation, self).__init__(oid=oid)
        self.num = contrast_num
        self.type = NIDM_CONTRAST_ESTIMATION
        self.prov_type = PROV['Activity']
        if label is not None:
            self.label = label
        else:
            self.label = "Contrast estimation: " + contrast_name
        # Only used when reading (so far)
        self.param_estimate = param_estimate

    def export(self, nidm_version):
        """
        Create prov graph.
        """
        self.add_attributes((
            (PROV['type'], self.type),
            (PROV['label'], self.label)))
