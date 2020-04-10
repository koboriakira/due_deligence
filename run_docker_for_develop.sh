docker run -it --rm \
  -v $(pwd)/due_deligence:/work/due_deligence \
  -v $(pwd)/tests:/work/tests \
  -v $(pwd)/logs:/work/logs \
  -v $(pwd)/sample:/work/sample \
  -v $(pwd)/setup.py:/work/setup.py \
  -v $(pwd)/requirements.txt:/work/requirements.txt \
  --name due_deligence \
  due_deligence_image
