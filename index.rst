.. Predictions Analyzer documentation master file, created by
   sphinx-quickstart on Mon Jan 11 07:40:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Predictions Analyzer's documentation!
================================================

To install

pip install predictions-analyzer-tpmeli

from predictions-analyzer-tpmeli import segmentation_analysis

I'm removing the '-tpmeli' from the install and module name soon and open-sourcing
this project.

segmentation_analysis Examples
====================

Can be used to predict bias in predictions with analyze_preds_bias(true_list, pred_list)

.. image:: docs/imgs/analyze_preds_bias.png

Can also be used to analyze individual predictions with show_many_wrongs_mask(true_list, pred_list)

.. image:: docs/imgs/show_many_wrongs_mask.png

====================

.. automodule:: segmentation_analysis
   :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

