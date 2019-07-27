#!/usr/bin/env bash
source activate Diploma
uvicorn main:app --reload # --host=0.0.0.0