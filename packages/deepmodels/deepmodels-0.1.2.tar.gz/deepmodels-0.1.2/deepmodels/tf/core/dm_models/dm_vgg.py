"""DeepModels version of VGG16.
"""

import os

from deepmodels.tf.core import commons
from deepmodels.tf.core import model_zoo
from deepmodels.shared.tools import data_manager


class VGGDM(model_zoo.NetworkDM):
  """DeepModels version of vgg, including 16 and 19.
  """
  vggm_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[commons.ModelTypes.VGG_M],
      model_type=commons.ModelTypes.VGG_M,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)
  vgg16_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[commons.ModelTypes.VGG16],
      model_type=commons.ModelTypes.VGG16,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)
  vgg19_params = commons.ModelParams(
      model_name=commons.ModelTypes.model_names[commons.ModelTypes.VGG19],
      model_type=commons.ModelTypes.VGG19,
      input_img_width=224,
      input_img_height=224,
      cls_num=1000)

  def __init__(self, net_type=commons.ModelTypes.VGG16):
    if net_type == commons.ModelTypes.VGG16:
      self.net_params = self.vgg16_params
    elif net_type == commons.ModelTypes.VGG19:
      self.net_params = self.vgg19_params
    elif net_type == commons.ModelTypes.VGG_M:
      self.net_params = self.vggm_params
    else:
      raise ValueError("incorrect vgg type.")
    self.net_graph_fn = ""
    self.net_weight_fn = model_zoo.get_builtin_net_weights_fn(
        self.net_params.model_type)

  def get_label_names(self):
    proj_dir = data_manager.get_project_dir()
    #TODO(jiefeng): check if vgg19 uses the same labels.

    label_fn = os.path.join(proj_dir, "tf/models/vgg/vgg_16_labels.txt")
    label_name_dict = {}
    with open(label_fn, "r") as f:
      label_str = f.read()
      label_name_dict = eval(label_str)
    return label_name_dict
