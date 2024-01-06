.. _core:

Core App
========

Views
-----

HomeView
^^^^^^^^

.. autoclass:: core.views.HomeView
   :members:
   :undoc-members:
   :show-inheritance:

DashboardView
^^^^^^^^^^^^^

.. autoclass:: core.views.DashboardView
   :members:
   :undoc-members:
   :show-inheritance:

about_us
^^^^^^^^

.. autofunction:: core.views.about_us

Signals
-------

post_save_signal
^^^^^^^^^^^^^^^^

.. autofunction:: core.views.log_create_update

pre_delete_signal
^^^^^^^^^^^^^^^^^

.. autofunction:: core.views.log_delete

Models
------

BaseModel
^^^^^^^^^

.. autoclass:: core.models.BaseModel
   :members:
   :undoc-members:
   :show-inheritance:

AuditLog
^^^^^^^^

.. autoclass:: core.models.AuditLog
   :members:
   :undoc-members:
   :show-inheritance:
