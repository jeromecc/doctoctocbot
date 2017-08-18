#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Implement the database.

Author: Anatole Hanniet.
License: Mozilla Public License (2.0), see 'LICENSE' for details.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Parent class for objects to persist in database
Base = declarative_base()

# Database session factory
engine = create_engine('DATABASE_URL')
Session = sessionmaker(bind=engine)
