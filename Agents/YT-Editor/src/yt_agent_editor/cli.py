from __future__ import annotations

import argparse
import shlex
from pathlib import Path

from yt_agent_editor.pipeline import run_analysis
from yt_agent_editor.transcript import merge_transcript_segments, parse_srt_file
from yt_agent_editor.analysis import generate_chapters, generate_youtube_description
from yt_agent_editor.export.reports import write_youtube_description
from yt_agent_editor.video.concatenate_video import concatenate_intro_with_video
from yt_agent_editor.video.extract_clips import extract_hook_clips, load_hooks
from yt_agent_editor.video.make_intro_montage import make_intro_montage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="yt-agent-editor")
    subparsers = parser.add_subparsers(dest="command")

    analyze = subparsers.add_parser("analyze", help="Analyze a video and SRT transcript.")
    analyze.add_argument("--video", type=Path, required=True)
    analyze.add_argument("--srt", type=Path, required=True)
    analyze.add_argument("--output-dir", type=Path, default=Path("outputs/reports"))
    analyze.add_argument("--mode", choices=["mock", "real"], default="mock")
    analyze.set_defaults(func=cmd_analyze)

    make_intro = subparsers.add_parser("make-intro", help="Extract hooks and build an intro montage.")
    make_intro.add_argument("--video", type=Path, required=True)
    make_intro.add_argument("--hooks", type=Path, required=True)
    make_intro.add_argument("--dry-run", action="store_true")
    make_intro.set_defaults(func=cmd_make_intro)

    full = subparsers.add_parser("full", help="Run analysis, hook extraction, and intro assembly.")
    full.add_argument("--video", type=Path, required=True)
    full.add_argument("--srt", type=Path, required=True)
    full.add_argument("--dry-run", action="store_true")
    full.set_defaults(func=cmd_full)

    export_description = subparsers.add_parser(
        "export-description", help="Export a mock YouTube description from an SRT file."
    )
    export_description.add_argument("--srt", type=Path, required=True)
    export_description.add_argument("--output", type=Path, default=Path("outputs/reports/youtube_description.txt"))
    export_description.set_defaults(func=cmd_export_description)

    return parser


def cmd_analyze(args: argparse.Namespace) -> None:
    run_analysis(video_path=args.video, srt_path=args.srt, output_dir=args.output_dir, mode=args.mode)
    print(f"Wrote reports to {args.output_dir}")


def cmd_make_intro(args: argparse.Namespace) -> None:
    hooks = load_hooks(args.hooks)
    commands = extract_hook_clips(video_path=args.video, hooks=hooks, dry_run=args.dry_run)
    clip_paths = [Path(command[-1]) for command in commands]
    montage_command = make_intro_montage(clips=clip_paths, dry_run=args.dry_run)
    for command in [*commands, montage_command]:
        print(shlex.join(command))


def cmd_full(args: argparse.Namespace) -> None:
    run_analysis(video_path=args.video, srt_path=args.srt)
    hooks = load_hooks(Path("outputs/reports/hook_candidates.json"))
    commands = extract_hook_clips(video_path=args.video, hooks=hooks, dry_run=args.dry_run)
    clip_paths = [Path(command[-1]) for command in commands]
    montage_command = make_intro_montage(clips=clip_paths, dry_run=args.dry_run)
    final_command = concatenate_intro_with_video(
        intro_path=Path("outputs/final/intro_montage.mp4"),
        video_path=args.video,
        dry_run=args.dry_run,
    )
    for command in [*commands, montage_command, final_command]:
        print(shlex.join(command))


def cmd_export_description(args: argparse.Namespace) -> None:
    blocks = merge_transcript_segments(parse_srt_file(args.srt))
    chapters = generate_chapters(blocks)
    description = generate_youtube_description(blocks, chapters)
    write_youtube_description(args.output, description)
    print(f"Wrote {args.output}")


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
