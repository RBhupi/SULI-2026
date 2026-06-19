TABLE_GROUPS = {

    "cell_events": {
        "Lifecycle": ["event_type", "event_group_id", "is_dominant"],
        "Cells": ["source_cell_uid", "target_cell_uid"],
        "Cost": ["cost"]
    },

    "cell_tracks": {
        "Track": ["cell_uid", "duration_seconds", "n_scans"],
        "Origin": ["origin_type"],
        "Termination": ["termination_type"],
        "Intensity": ["max_reflectivity", "max_area_sqkm"]
    },

    "cells_by_scan": {
        "Core": ["cell_uid", "scan_time"],
        "Intensity": ["radar_reflectivity_max"],
        "Motion": ["radar_velocity_mean"],
        "Lifecycle": ["is_merge_target_here", "is_split_target_here", "age_seconds"]
    },

    "cell_volume_stats": {
        "Reflectivity": ["dbz_max", "dbz_mean"],
        "Geometry": ["cell_area_km2", "cell_volume_km3", "cell_top_m"],
        "Polar": ["zdr_max", "rhohv_mean"],
        "Lightning": ["scan_time_unix"]
    },

    "xlma_stat_scan": {
        "Lightning": ["flash_count", "mean_flash_rate_per_min"],
        "Energy": ["total_flash_energy"],
        "Altitude": ["max_source_alt_m"]
    }
}