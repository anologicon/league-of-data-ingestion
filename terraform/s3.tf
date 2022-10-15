provider "aws" {
    profile = "default"
    region = "us-east-1"
}

resource "aws_s3_bucket" "league-data-bronze" {
  bucket = "league-data-bronze"
}

resource "aws_s3_bucket" "league-data-silver" {
  bucket = "league-data-silver"
}

resource "aws_s3_bucket" "league-data-gold" {
  bucket = "league-data-gold"
}