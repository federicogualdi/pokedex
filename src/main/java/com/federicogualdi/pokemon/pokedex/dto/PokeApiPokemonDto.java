package com.federicogualdi.pokemon.pokedex.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class PokeApiPokemonDto {
    public String name;
    @JsonProperty("flavor_text_entries")
    public List<PokeApiPokemonFlavorTextEntriesDto> flavorTextEntries;
    public PokeApiPokemonHabitatDto habitat;
    @JsonProperty("is_legendary")
    public Boolean isLegendary;

    public PokeApiPokemonDto() {
    }

    @Override
    public String toString() {
        return "PokeApiPokemonDto{" + "name='" + name + '\'' + ", habitat=" + habitat + ", isLegendary=" + isLegendary + '}';
    }
}


