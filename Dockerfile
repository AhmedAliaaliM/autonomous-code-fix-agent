# Sandbox image the agent operates inside when editing/testing a target repo.
# Kept separate from any "runner" image that hosts the agent loop itself —
# this one only needs to build and test arbitrary small Python repos.
FROM python:3.11-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recursive git \
    && rm -rf /var/lib/apt/lists/*

# Target repos install their own deps at runtime via their requirements.txt,
# so this image stays minimal on purpose.

CMD ["bash"]
