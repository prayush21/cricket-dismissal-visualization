"use client";

import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { api } from "./api";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

type PlayerStats = {
  max_runs_scored: number;

  dismissals_on_ball: { [key: string]: number };
  dismissals_on_run: { [key: string]: number };
  matches_played: number;
};

const Dashboard = () => {
  const [format, setFormat] = useState("ODI");
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [playerStats, setPlayerStats] = useState<PlayerStats | null>(null);

  const [activeTab, setActiveTab] = useState<"ball" | "run">("ball");

  useEffect(() => {
    fetchTeams();
  }, [format]);

  useEffect(() => {
    if (selectedTeam) {
      fetchPlayers();
    }
  }, [selectedTeam]);

  useEffect(() => {
    if (selectedPlayer) {
      fetchPlayerStats();
    }
  }, [selectedPlayer]);

  const fetchTeams = async () => {
    try {
      const response = await api.get(`/api/v2/teams?format=${format}`);
      setTeams(response.data);
    } catch (error) {
      console.error("Error fetching teams:", error);
    }
  };

  const fetchPlayers = async () => {
    try {
      const response = await api.get(
        `/api/v2/players?format=${format}&team=${selectedTeam}`
      );
      setPlayers(response.data);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  const fetchPlayerStats = async () => {
    try {
      const response = await api.get(
        `/api/v2/player-stats?format=${format}&player=${selectedPlayer}`
      );
      setPlayerStats(response.data);
    } catch (error) {
      console.error("Error fetching player stats:", error);
    }
  };

  // const chartDataForBalls = {
  //   labels: playerStats ? Object.keys(playerStats.dismissals_on_ball) : [],
  //   datasets: [
  //     {
  //       label: "Dismissal Counts",
  //       data: playerStats ? Object.values(playerStats.dismissals_on_ball) : [],
  //       backgroundColor: "rgba(75, 192, 192, 0.6)",
  //       borderColor: "rgba(75, 192, 192, 1)",
  //       borderWidth: 1,
  //     },
  //   ],
  // };

  const createChartData = (data: { [key: string]: number }) => ({
    labels: Object.keys(data),
    datasets: [
      {
        label: "Dismissal Counts",
        data: Object.values(data),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  });

  // const chartDataForRuns = {
  //   labels: playerStats ? Object.keys(playerStats.dismissals_on_ball) : [],
  //   datasets: [
  //     {
  //       label: "Dismissal Counts",
  //       data: playerStats ? Object.values(playerStats.dismissals_on_ball) : [],
  //       backgroundColor: "rgba(75, 192, 192, 0.6)",
  //       borderColor: "rgba(75, 192, 192, 1)",
  //       borderWidth: 1,
  //     },
  //   ],
  // };

  const chartOptions = (text: string) => {
    return {
      responsive: true,
      plugins: {
        legend: {
          position: "top" as const,
          labels: {
            color: "white",
          },
        },
        title: {
          display: true,
          text: text,
          color: "white",
        },
      },
      scales: {
        x: {
          ticks: { color: "white" },
          grid: { color: "rgba(255, 255, 255, 0.1)" },
        },
        y: {
          ticks: { color: "white" },
          grid: { color: "rgba(255, 255, 255, 0.1)" },
        },
      },
    };
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-gray-800 rounded-lg shadow-lg text-white">
      <h1 className="text-3xl font-bold mb-6 text-center">Cricket Dashboard</h1>
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Format</label>
        <div className="flex space-x-4">
          {["ODI", "T20", "IPL"].map((f) => (
            <label key={f} className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio text-blue-600"
                name="format"
                value={f}
                checked={format === f}
                onChange={(e) => setFormat(e.target.value)}
              />
              <span className="ml-2">{f}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <label htmlFor="team" className="block text-sm font-medium mb-2">
          Team
        </label>
        <select
          id="team"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md bg-gray-700 text-white"
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
        >
          <option value="">Select a team</option>
          {teams.map((team) => (
            <option key={team} value={team}>
              {team}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <label htmlFor="player" className="block text-sm font-medium mb-2">
          Player
        </label>
        <select
          id="player"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md bg-gray-700 text-white"
          value={selectedPlayer}
          onChange={(e) => setSelectedPlayer(e.target.value)}
        >
          <option value="">Select a player</option>
          {players.map((player) => (
            <option key={player} value={player}>
              {player}
            </option>
          ))}
        </select>
      </div>

      {/* {playerStats && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Player Statistics</h2>
          <Bar data={chartDataForBalls} options={chartOptions(false)} />
        </div>
      )}

      {playerStats && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Player Statistics</h2>
          <Bar data={chartDataForRuns} options={chartOptions(true)} />
        </div>
      )} */}

      {playerStats && (
        <div className="mt-8 space-y-8">
          <h2 className="text-2xl font-bold mb-4">Player Statistics</h2>
          <div className="bg-gray-700 rounded-lg overflow-hidden">
            <div className="flex border-b border-gray-600">
              <button
                className={`flex-1 py-2 px-4 text-center ${
                  activeTab === "ball" ? "bg-blue-600" : "hover:bg-gray-600"
                }`}
                onClick={() => setActiveTab("ball")}
              >
                Dismissals by Ball
              </button>
              <button
                className={`flex-1 py-2 px-4 text-center ${
                  activeTab === "run" ? "bg-blue-600" : "hover:bg-gray-600"
                }`}
                onClick={() => setActiveTab("run")}
              >
                Dismissals by Run
              </button>
            </div>
            <div className="p-4">
              {activeTab === "ball" && (
                <Bar
                  data={createChartData(playerStats.dismissals_on_ball)}
                  options={chartOptions(
                    `Dismissal Counts by Ball for ${selectedPlayer} in ${format}`
                  )}
                />
              )}
              {activeTab === "run" && (
                <Bar
                  data={createChartData(playerStats.dismissals_on_run)}
                  options={chartOptions(
                    `Dismissal Counts by Run for ${selectedPlayer} in ${format}`
                  )}
                />
              )}
            </div>
          </div>
          {/* ... (match statistics code) */}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
