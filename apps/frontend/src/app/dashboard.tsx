"use client";

import axios from "axios";
import React, { useState, useEffect } from "react";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:5000",
});

const Dashboard = () => {
  const [format, setFormat] = useState("ODI");
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState("");

  useEffect(() => {
    fetchTeams();
  }, [format]);

  useEffect(() => {
    if (selectedTeam) {
      fetchPlayers();
    }
  }, [selectedTeam]);

  const fetchTeams = async () => {
    try {
      const response = await api.get(`/teams?format=${format}`);
      setTeams(response.data);
    } catch (error) {
      console.error("Error fetching teams:", error);
    }
  };

  const fetchPlayers = async () => {
    try {
      const response = await api.get(
        `/players?format=${format}&team=${selectedTeam}`
      );
      setPlayers(response.data);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  return (
    <div className="w-full max-w-md">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Format
        </label>
        <div className="flex space-x-4">
          {["ODI", "T20", "IPL"].map((f) => (
            <label key={f} className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
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

      <div className="mb-4">
        <label
          htmlFor="team"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Team
        </label>
        <select
          id="team"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base text-black border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
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

      <div className="mb-4">
        <label
          htmlFor="player"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Player
        </label>
        <select
          id="player"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base text-black border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
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
    </div>
  );
};

export default Dashboard;
