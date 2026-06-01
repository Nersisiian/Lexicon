#!/usr/bin/env python3
"""Seed demo data into the intake database for local development."""
import asyncio
from intake_gateway.config import Settings
from intake_gateway.repository import DocumentRepository
from intake_gateway.service import IntakeService
# omitted full import chain for brevity, in reality it would bootstrap DI

async def main():
    # placeholder: would create a sample document via service
    pass

if __name__ == "__main__":
    asyncio.run(main())